from django.db import models
from django.db.models.query import QuerySet
from django.core import validators
from django.contrib.auth.models import User, UserManager, Group
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils.translation import ugettext as _
from django.utils.timezone import now
from easy_thumbnails.fields import ThumbnailerImageField
from userena.models import UserenaBaseProfile
from model_utils import FieldTracker
from model_utils.managers import PassThroughManager
import os
import re

def factory_userprofile_upload_to(basename):
    def update_to(instance, filename):
        fbasename = os.path.basename(filename)
        fbname ,extension = fbasename.split('.')
        path = "%(prefix)s/%(date)s/%(user_id)d/%(fbname)s.%(extension)s" % {
            'prefix': 'userprofile',
            'date': now().strftime("%Y%m%d"),
            'user_id': instance.user.pk,
            'fbname': basename,
            'extension': extension
        }
        return path
    return update_to

def upload_to_cover(instance, filename):
    extension = filename.split('.')[-1].lower()
    path = "users/%d" % instance.user.pk
    fname = 'cover'
    return '%(path)s/%(filename)s.%(extension)s' % {'path':path,
                                                    'filename': fname,
                                                    'extension':extension,
                                                   }

class PlayerQuerySet(QuerySet):

    def by_profile_with(self, **kwargs):
        kwargs = {('gamecenter_profile__%s' % qf ): qv for qf, qv in kwargs.items()}

        return self.filter(
            **kwargs
        )

    def published(self):
        return self.filter(is_active=True)

class PlayerManager(UserManager, PassThroughManager):

    def create_user(self,
                    username,
                    email=None, phone=None,
                    password=None,
                    **extra_fields):
        user = super(PlayerManager, self).create_user(username=username,
                                                      password=password,
                                                      **extra_fields)
        group_player, _is_new = Group.objects.get_or_create(name='player')
        user.groups.add(group_player)
        Profile.objects.create(user=user, email=email, phone=phone)
        return user

class Player(User):

    objects = PlayerManager.for_queryset_class(PlayerQuerySet)()

    @property
    def profile(self):
        return self.gamecenter_profile

    @profile.setter
    def profile(self, value):
        self.gamecenter_profile = value

    class Meta:
        proxy = True

class Profile(UserenaBaseProfile):

    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='gamecenter_profile')

    @property
    def icon(self):
        return self.mugshot

    @icon.setter
    def icon(self, value):
        self.mugshot = value

    cover = ThumbnailerImageField(_('cover image'),
                                  blank=True,
                                  upload_to=factory_userprofile_upload_to('cover'),
                                  help_text=_("A personal cover image displayed in your profile"),
    )

    email = models.EmailField(verbose_name=_('register email'), default='',
                              error_messages={'null': _('should not be empty')},
                              unique=True)

    phone = models.CharField(verbose_name=_('register phone'), max_length=20, unique=True, default='',
                             help_text=_('Required. 20 characters or fewer. numbers and '
                                         '+/-/ characters'),
                             error_messages={'null': _('should not be empty')},
                             validators=[
                                 validators.RegexValidator(re.compile('^[\d.+-]+$'),
                                                           _('invalid phone number.'), 'invalid')
                             ])

    tracker = FieldTracker()

    bookmarks = models.ManyToManyField('warehouse.Package', verbose_name=_('bookmarks'))

# Hack to override mugshot.upload_to and mugshot.generate_filename
# In Django, this is not permitted for override django.models.Model attributes
Profile.__dict__.get('mugshot').field.upload_to =\
    Profile.__dict__.get('mugshot').field.generate_filename =\
    factory_userprofile_upload_to('icon')

@receiver(post_delete, sender=User)
def post_delete_user(sender, instance, *args, **kwargs):
    instance.gamecenter_profile.delete()

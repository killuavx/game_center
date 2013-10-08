from django.db import models
from django.db.models.query import QuerySet
from django.core import validators
from django.contrib.auth.models import User, UserManager
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils.translation import ugettext as _
from easy_thumbnails.fields import ThumbnailerImageField
from userena.models import UserenaBaseProfile
from model_utils import FieldTracker
from model_utils.managers import PassThroughManager
import re

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
                                  upload_to=upload_to_cover,
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

@receiver(post_delete, sender=User)
def post_delete_user(sender, instance, *args, **kwargs):
    instance.gamecenter_profile.delete()

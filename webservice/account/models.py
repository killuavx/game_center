import os
import re

from django.contrib.auth import get_user_model
from django.db import models
from django.core import validators
from django.conf import settings
from django.contrib.auth.models import (AbstractUser as UserBase)
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from easy_thumbnails.fields import ThumbnailerImageField
from guardian.shortcuts import get_perms
from model_utils import FieldTracker

from account.managers import UserQuerySet, UserManager, ProfileManager


def factory_userprofile_upload_to(basename):
    def update_to(instance, filename):
        fbasename = os.path.basename(filename)
        fbname, extension = fbasename.split('.')
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
    return '%(path)s/%(filename)s.%(extension)s' % {'path': path,
                                                    'filename': fname,
                                                    'extension': extension,
    }


class User(UserBase):
    objects = UserManager.for_queryset_class(UserQuerySet)()

    @property
    def profile(self):
        return self.gamecenter_profile

    @profile.setter
    def profile(self, value):
        self.gamecenter_profile = value

    class Meta:
        #proxy = True
        db_table = 'auth_user'


PROFILE_PERMISSIONS = (
    ('view_profile', 'Can view profile'),
)


class ProfileBase(models.Model):
    PRIVACY_CHOICES = (
        ('open', _('Open')),
        ('registered', _('Registered')),
        ('closed', _('Closed')),
    )

    mugshot = ThumbnailerImageField(_('mugshot'),
                                    blank=True,
                                    help_text=_('A personal image displayed in your profile.'))

    privacy = models.CharField(_('privacy'),
                               max_length=15,
                               choices=PRIVACY_CHOICES,
                               default=getattr(settings, 'USERENA_DEFAULT_PRIVACY', True),
                               help_text=_('Designates who can view your profile.'))

    class Meta:
        abstract = True
        permissions = PROFILE_PERMISSIONS

    def __str__(self):
        return 'Profile of %(username)s' % {'username': self.user.username}

    def get_mugshot_url(self):
        """
        Returns the image containing the mugshot for the user.

        """
        # First check for a mugshot and if any return that.
        if self.mugshot:
            return self.mugshot.url

        return None

    def get_full_name_or_username(self):
        return self.user.username

    def can_view_profile(self, user):
        """
        Can the :class:`User` view this profile?

        Returns a boolean if a user has the rights to view the profile of this
        user.

        Users are divided into four groups:

            ``Open``
                Everyone can view your profile

            ``Closed``
                Nobody can view your profile.

            ``Registered``
                Users that are registered on the website and signed
                in only.

            ``Admin``
                Special cases like superadmin and the owner of the profile.

        Through the ``privacy`` field a owner of an profile can define what
        they want to show to whom.

        :param user:
            A Django :class:`User` instance.

        """
        # Simple cases first, we don't want to waste CPU and DB hits.
        # Everyone.
        if self.privacy == 'open':
            return True
        # Registered users.
        elif self.privacy == 'registered' \
            and isinstance(user, get_user_model()):
            return True

        # Checks done by guardian for owner and admins.
        elif 'view_profile' in get_perms(user, self):
            return True

        # Fallback to closed profile.
        return False


class Profile(ProfileBase):

    objects = ProfileManager()

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
                                  upload_to=factory_userprofile_upload_to(
                                      'cover'),
                                  help_text=_(
                                      "A personal cover image displayed in your profile"),
    )

    email = models.EmailField(verbose_name=_('register email'),
                              default='',
                              error_messages={'null': _('should not be empty')},
                              unique=True)

    phone = models.CharField(verbose_name=_('register phone'),
                             max_length=20,
                             unique=True,
                             default='',
                             help_text=_(
                                 'Required. 20 characters or fewer. numbers and '
                                 '+/-/ characters'),
                             error_messages={'null': _('should not be empty')},
                             validators=[
                                 validators.RegexValidator(
                                     re.compile('^[\d.+-]+$'),
                                     _('invalid phone number.'), 'invalid')
                             ])

    tracker = FieldTracker()

    bookmarks = models.ManyToManyField('warehouse.Package',
                                       blank=True,
                                       verbose_name=_('bookmarks'))

    signup_date = models.DateTimeField(_('sign up date'),
                                       default=now,
                                       auto_created=True,
                                       editable=False)

    update_date = models.DateTimeField(_('latest update date'),
                                       default=now,
                                       editable=False,
                                       blank=True,
                                       auto_created=True,
                                       auto_now=True)


# Hack to override mugshot.upload_to and mugshot.generate_filename
# In Django, this is not permitted for override django.models.Model attributes
Profile.__dict__.get('mugshot').field.upload_to = \
    Profile.__dict__.get('mugshot').field.generate_filename = \
    factory_userprofile_upload_to('icon')


@receiver(post_delete, sender=User)
def post_delete_user(sender, instance, *args, **kwargs):
    try:
        instance.gamecenter_profile.delete()
    except Profile.DoesNotExist:
        pass


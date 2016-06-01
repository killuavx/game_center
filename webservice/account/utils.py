# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.contrib.auth.models import SiteProfileNotAvailable
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import get_model
from django.contrib.auth import get_user


try:
    from hashlib import sha1 as sha_constructor
except ImportError:
    from django.utils.hashcompat import sha_constructor
import random


def get_profile_model():
    """
    Return the model class for the currently-active user profile
    model, as defined by the ``AUTH_PROFILE_MODULE`` setting.

    :return: The model that is used as profile.

    """
    if (not hasattr(settings, 'AUTH_PROFILE_MODULE')) or \
            (not settings.AUTH_PROFILE_MODULE):
        raise SiteProfileNotAvailable

    profile_mod = get_model(*settings.AUTH_PROFILE_MODULE.split('.'))
    if profile_mod is None:
        raise SiteProfileNotAvailable
    return profile_mod


def generate_sha1(string, salt=None):
    """
    Generates a sha1 hash for supplied string. Doesn't need to be very secure
    because it's not used for password checking. We got Django for that.

    :param string:
        The string that needs to be encrypted.

    :param salt:
        Optionally define your own salt. If none is supplied, will use a random
        string of 5 characters.

    :return: Tuple containing the salt and hash.

    """
    if not salt:
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
    hash = sha_constructor(salt+str(string)).hexdigest()

    return (salt, hash)


def get_datetime_now():
    """
    Returns datetime object with current point in time.

    In Django 1.4+ it uses Django's django.utils.timezone.now() which returns
    an aware or naive datetime that represents the current point in time
    when ``USE_TZ`` in project's settings is True or False respectively.
    In older versions of Django it uses datetime.datetime.now().

    """
    try:
        from django.utils import timezone
        return timezone.now() # pragma: no cover
    except ImportError: # pragma: no cover
        return datetime.datetime.now()


PROFILE_EMAIL_DEFAULT_HOST = 'uc.ccplay.com.cn'


def generate_random_email(host=PROFILE_EMAIL_DEFAULT_HOST):
    identification = sha_constructor(str(random.random()).encode('utf-8')) \
                         .hexdigest()[:10]
    return "%s@%s" %(identification, host)


user_model_label = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    get_user_model = lambda: User


def unique_value(queryset, field, value, segment='-'):
    i = 0
    while True:
        if i > 0:
            if i > 1:
                value = value.rsplit(segment, 1)[0]
            value = "%s%s%s" % (value, segment, i)
        try:
            queryset.get(**{field: value})
        except ObjectDoesNotExist:
            break
        i += 1
    return value


def unique_email_value(queryset, field, email, segment='_'):
    i = 0
    value, host = email.split('@')
    while True:
        if i > 0:
            if i > 1:
                value = value.rsplit(segment, 1)[0]
            value = "%s%s%s" % (value, segment, i)
            email = "%s@%s" %(value, host)
        try:
            queryset.get(**{field: email})
        except ObjectDoesNotExist:
            break
        i += 1
    return email


# -*- coding: utf-8 -*-
from copy import deepcopy
from django.contrib.auth import get_backends, user_login_failed, _clean_credentials
from toolkit.helpers import import_from


def mezzanine_auth_backend():
    return import_from('mezzanine.core.auth_backends.MezzanineBackend')


def filter_keys(backend, data):
    if not isinstance(backend, mezzanine_auth_backend()):
        return

    for k in ('app', 'check_password'):
        try:
            data.pop(k)
        except KeyError:
            pass


def ignore_authenticate(backend, credentials):
    if isinstance(backend, mezzanine_auth_backend()):
        if 'app' in credentials:
            return True

        if 'check_password' in credentials:
            return True

    return False



def authenticate(**credentials):
    """
        overwrite authenticate to fix mezzanine.core.auth_backends.MezzanineBackend kwargs error
    If the given credentials are valid, return a User object.
    """
    backends = get_backends()
    for backend in backends:
        try:
            _credentials = deepcopy(credentials)
            if isinstance(backend, mezzanine_auth_backend()):
                if ignore_authenticate(backend, _credentials):
                    continue
            filter_keys(backend, _credentials)
            user = backend.authenticate(**_credentials)
        except TypeError:
            # This backend doesn't accept these credentials as arguments. Try the next one.
            continue

        if user is None:
            continue
            # Annotate the user object with the path of the backend.
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        return user

    # The credentials supplied are invalid to all backends, fire signal
    user_login_failed.send(sender=__name__,
                           credentials=_clean_credentials(credentials))

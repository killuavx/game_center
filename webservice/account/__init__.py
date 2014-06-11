# -*- coding: utf-8 -*-
from copy import deepcopy
from django.contrib.auth import get_backends, user_login_failed, _clean_credentials
from toolkit.helpers import import_from


def filter_keys(data):
    try:
        data.pop('app')
    except KeyError:
        pass


def authenticate(**credentials):
    """
        overwrite authenticate to fix mezzanine.core.auth_backends.MezzanineBackend kwargs error
    If the given credentials are valid, return a User object.
    """
    for backend in get_backends():
        try:
            _credentials = credentials
            if isinstance(backend, import_from('mezzanine.core.auth_backends.MezzanineBackend')):
                _credentials = deepcopy(credentials)
                filter_keys(_credentials)
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

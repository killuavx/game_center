# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.contrib.auth import load_backend, user_login_failed, _clean_credentials, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import login, logout

APKSITE_BACKEND_PATH = 'apksite.backends.RemoteApiUserBackend'


def get_user(request):
    user = None
    try:
        user_id = request.session[SESSION_KEY]
        backend_path = request.session[BACKEND_SESSION_KEY]
    except KeyError:
        pass
    else:
        try:
            backend = load_backend(backend_path)
            user = backend.get_user(user_id)
        except ImproperlyConfigured:
            pass
    return user or AnonymousUser()

def authenticate(**credentials):
    backend = load_backend(APKSITE_BACKEND_PATH)
    user = None
    try:
        user = backend.authenticate(**credentials)
    except PermissionDenied:
        return None

    if user is not None:
        # Annotate the user object with the path of the backend.
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        return user

    # The credentials supplied are invalid to all backends, fire signal
    user_login_failed.send(sender=__name__,
                           credentials=_clean_credentials(credentials))


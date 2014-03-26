# -*- coding: utf-8 -*-

try:
    from threading import local, current_thread
except ImportError:
    from django.utils._threading_local import local, currentThread as current_thread

_thread_locals = {}

def set_current_request(request):
    _thread_locals.setdefault(current_thread(), dict())
    _thread_locals[current_thread()].update(dict(
        request=request,
    ))

def get_current_request():
    _thread_locals.setdefault(current_thread(), dict())
    return _thread_locals[current_thread()].get('request', None)

def get_current_response():
    _thread_locals.setdefault(current_thread(), dict())
    return _thread_locals[current_thread()].get('response', None)

class ThreadLocals(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        _thread_locals.setdefault(current_thread(), dict())
        _thread_locals[current_thread()].update(dict(
            request=request,
            response=None
        ))

    def process_response(self, request, response):
        _thread_locals.setdefault(current_thread(), dict())
        _thread_locals[current_thread()].update(dict(
            request=request,
            response=response
        ))
        return response


from django.utils.functional import SimpleLazyObject
from django.contrib import auth
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


def get_user(request):
    token_auth = TokenAuthentication()
    try:
        result = token_auth.authenticate(request)
        user, token = result
        request._cached_user = user
    except (AuthenticationFailed, TypeError):
        pass

    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user


class TokenAuthenticationMiddleware(object):

    def process_request(self, request):

        request.user = SimpleLazyObject(lambda: get_user(request))


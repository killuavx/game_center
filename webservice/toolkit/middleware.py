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
    return _thread_locals[current_thread()].get('request', None)

def get_current_response():
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

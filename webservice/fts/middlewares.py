# -*- coding: utf-8 -*-
try:
    from threading import local, current_thread
except ImportError:
    from django.utils._threading_local import local, currentThread as current_thread

_thread_locals = {}

def set_current_request( request ):
    _thread_locals[current_thread()] = request

def get_current_request():
    return _thread_locals[current_thread()]


class ThreadLocals(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        _thread_locals[current_thread()] = request

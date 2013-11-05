# -*- coding: utf-8 -*-
from collections import namedtuple
from os.path import join
import tempfile

from django.test import Client
from behave.matchers import register_type

from toolkit.middleware import get_current_response


def str2empty(s):
    if s.upper() == 'NONE':
        return None
    else:
        return s


def in2boolean(s):
    is_ = s.split(" ")
    if is_[0].lower() == 'not':
        return False
    else:
        return True


def pub2boolean(s):
    s = s.lower()
    if s == 'published':
        return True
    elif s == 'unpublished':
        return False
    return None


def upper(s):
    return s.upper()


def in_out(s):
    if not s in ('in', 'out'):
        raise Exception('match error')
    elif s == 'in':
        return True
    else:
        return False


register_type(**{
    'pub?': pub2boolean,
    'in?out': in_out,
    'in?': in2boolean,
    'be?': in2boolean,
    'n?s': str2empty,
    'upper': upper
})


StatusCode = namedtuple('StatusCode', ['code', 'reason'])


class HackBrowserFromClient(Client):

    @property
    def response(self):
        return get_current_response()

    @property
    def response_content(self):
        return self.response.content.decode('utf-8')

    @property
    def status_code(self):
        response = self.response
        reason = ''
        if hasattr(response, 'status_text'):
            reason = response.status_text
        return StatusCode(
            code=response.status_code,
            reason=reason
        )

    @property
    def html(self):
        return self.response_content

    def visit(self, url):
        self.get(url)

    def is_text_present(self, text):
        return text in self.response_content

    def screenshot(self, name):
        try:
            text = self.html
        except:
            return None

        (fd, full_name) = tempfile.mkstemp(prefix=name, suffix='.txt')
        with open(full_name, '+w') as file:
            file.write(text)
        return full_name


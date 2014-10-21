# -*- coding: utf-8 -*-
from mezzanine.conf import settings
from django.core.exceptions import ValidationError


class AccountUsernameForbiddenValidator(object):

    code = 'forbidden'

    message = "您的注册名有非法词"

    words = None

    def __init__(self, words=None, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.code = code
        self.words = words if words else settings.GC_ACCOUNT_USERNAME_FORBIDDEN_WORDS

    def __call__(self, value):
        words = self.words() if callable(self.words) else self.words
        val = value.lower()
        for w in words:
            if w in val:
                raise ValidationError(self.message % {'name': w}, code=self.code)



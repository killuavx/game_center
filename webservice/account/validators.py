# -*- coding: utf-8 -*-
import re
from mezzanine.conf import settings
from django.core.exceptions import ValidationError
from django.core import validators


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


phone_re = re.compile(r"^([0-9]{3,4})?-?(1[3-9][0-9]{0,9})$")
validate_phone = validators.RegexValidator(phone_re, '请填写有效手机号码', 'invalid')


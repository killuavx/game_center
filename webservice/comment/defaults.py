# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from toolkit.helpers import register_setting


register_setting(
    name="GC_COMMENT_FORBIDDEN_WORDS",
    description=_("评论禁止的词汇，以空格分割" ),
    editable=True,
    default='',
    widget=forms.Textarea
)

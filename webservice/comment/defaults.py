# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from toolkit.helpers import register_setting


register_setting(
    name="GC_COMMENT_FORBIDDEN_WORDS",
    description="评论禁止的词汇，以换行、逗号、空格分割",
    editable=True,
    default='',
    widget=forms.Textarea
)

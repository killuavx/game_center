# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from toolkit.mz_helpers import register_setting
from django import forms


register_setting(
    name="GC_COMMENT_FORBIDDEN_WORDS",
    description="评论禁止的词汇，以换行、逗号、空格分割",
    editable=True,
    default='',
    widget=forms.Textarea
)

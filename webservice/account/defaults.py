# -*- coding: utf-8 -*-
from toolkit.helpers import register_setting


def _(t):
    return t


register_setting(
    name="GC_ACCOUNT_USERNAME_FORBIDDEN_WORDS",
    description=_("用户名禁用词" ),
    editable=False,
    default=[
        'administrator',
        'admin',
        '管理员',
        '虫虫管理员',
        '虫虫助手',
    ],
)


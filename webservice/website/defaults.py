# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting


register_setting(
    name="GC_WIDGET_HOME_CATEGORY_PACKAGE_PANEL_SLUGS",
    description="主站首页的分类游戏面板里，展示的分类",
    editable=True,
    default=",".join((
        'crack-game',
        'big-game',
        'cn-game',
        'online-game',
        'standalone-relaxation-game',
        'standalone-action-game',
    )),
)

register_setting(
    name="GC_CATEGORIES_DEFAULT_SLUG",
    description=_("分类游戏列表页面，当进入/categories/，指定一个分类展示游戏列表" ),
    editable=True,
    default='big-game',
)


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
    description=_("Category.slug, 分类游戏列表页面，当进入/categories/，指定一个分类展示游戏列表" ),
    editable=True,
    default='big-game',
)

register_setting(
    name="GC_TOPICS_MASTERPIECE_SLUG",
    description=_("Topic.slug, 巨作页面，指定一个专辑(topic)展示游戏列表" ),
    editable=True,
    default='masterpiece',
    )
register_setting(
    name="GC_TOPICS_VENDOR_SLUG",
    description=_("Topic.slug, 顶级开发商指定一个专辑(topic)展示warehouse.author列表" ),
    editable=True,
    default='spec-top-author',
    )

register_setting(
    name="GC_TOPICS_CHOICE_SLUG",
    description=_("Topic.slug，专辑页面，当进入/topics/，指定一个专辑(topic)展示专辑列表" ),
    editable=True,
    default='home-recommend-game',
    )

register_setting(
    name="GC_COMPLEX_PACKAGE_FILTER_TOPIC_SLUGS",
    description="对分类下应用列表筛选的专区列表",
    editable=True,
    default=",".join((
        'home-recommend-game',
        'basic-installed',
        'NONE'
    )),
    )

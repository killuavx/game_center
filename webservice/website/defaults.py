# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.utils.functional import SimpleLazyObject, empty

from mezzanine.conf import register_setting

register_setting(
    name="GC_HOST_NAME",
    description=_("主站域名" ),
    editable=True,
    default='www.ccplay.com.cn',
    )

register_setting(
    name="GC_FOOTER_CLIENT_DOWNLOAD_PACKAGE_NAME",
    description=_("分站页面Footer最新版本下载qrcode对应客户端包名" ),
    editable=True,
    default='',
)

class LazyIter(SimpleLazyObject):

    def __iter__(self):
        if self._wrapped is empty:
            return iter(self._setup())
        rtn = iter(self._wrapped)
        self._wrapped = empty
        return rtn

def _topic_setup():
    from taxonomy.models import Topic
    result = [(topic.slug, topic.name) for topic in Topic.objects.all()]
    result.insert(0, ('', '------'))
    return result

def _place_setup():
    from promotion.models import Place
    result = [(p.slug, p.help_text) for p in Place.objects.all()]
    result.insert(0, ('', '------'))
    return result

def _rankingtype_setup():
    from ranking.models import PackageRankingType
    result = [(r.slug, r.title) for r in PackageRankingType.objects.all()]
    return result


topic_choices = LazyIter(_topic_setup)
place_choices = LazyIter(_place_setup)
rankingtype_choices = LazyIter(_rankingtype_setup)

register_setting(
    name="GC_WEB_HOME_A1_PLACE_SLUG",
    description=_("主站首页,头部Banner的广告位置slug" ),
    editable=True,
    default='banner-web',
    choices=place_choices,
)

register_setting(
    name="GC_WEB_CRACK_A1_PLACE_SLUG",
    description=_("主站破解页面,头部Banner的广告位置slug" ),
    editable=True,
    default='banner-web-crack',
    choices=place_choices,
)

register_setting(
    name="GC_WEB_LATEST_A1_PLACE_SLUG",
    description=_("主站最新发布页面,头部Banner的广告位置slug" ),
    editable=True,
    default='banner-web-latest',
    choices=place_choices,
    )


register_setting(
    name="GC_WEB_HOME_T1_TOPIC_SLUG",
    description=_("主站首页,行1列2软件列表专区slug" ),
    editable=True,
    default='charge-recommend',
    choices=topic_choices
)

register_setting(
    name="GC_WEB_HOME_T2_TOPIC_SLUG",
    description=_("主站首页,行1列3软件列表专区slug" ),
    editable=True,
    default='network-game',
    choices=topic_choices
)

register_setting(
    name="GC_WEB_HOME_A2_PLACE_SLUG",
    description=_("主站首页,行2列1广告位slug" ),
    editable=True,
    default='',
    choices=place_choices,
)

register_setting(
    name="GC_WEB_HOME_A3_PLACE_SLUG",
    description=_("主站首页,行2列2广告位slug" ),
    editable=True,
    default='',
    choices=place_choices,
)

register_setting(
    name="GC_WEB_HOME_A4_PLACE_SLUG",
    description=_("主站首页,行4列1广告位slug" ),
    editable=True,
    default='',
    choices=place_choices,
)

register_setting(
    name="GC_WEB_HOME_A5_PLACE_SLUG",
    description=_("主站首页,行4列2广告位slug" ),
    editable=True,
    default='',
    choices=place_choices,
)

register_setting(
    name="GC_WEB_HOME_T3_TOPIC_SLUG",
    description=_("主站首页,行4合集位slug" ),
    editable=True,
    default='spec-choice-topic',
    choices=topic_choices
    )

register_setting(
    name="GC_WEB_HOME_T4_PLACE_SLUG",
    description=_("主站首页,行6列1广告位slug" ),
    editable=True,
    default='',
    choices=topic_choices,
)

register_setting(
    name="GC_WEB_HOME_A6_PLACE_SLUG",
    description=_("主站首页,行6列2广告位slug" ),
    editable=True,
    default='',
    choices=place_choices,
)

register_setting(
    name="GC_WEB_HOME_A7_PLACE_SLUG",
    description=_("主站首页,行6合集位slug" ),
    editable=True,
    default='',
    choices=place_choices,
)

register_setting(
    name="GC_WEB_HOME_A8_PLACE_SLUG",
    description=_("主站首页,行7bbs新手帖广告位置slug" ),
    editable=True,
    default='',
    choices=place_choices,
)


register_setting(
    name="GC_WEB_HOME_F1_RSS_LINK",
    description=_("主站首页,论坛热帖rss地址" ),
    editable=True,
    default='http://bbs.ccplay.com.cn/api.php?mod=rss&bid=45',
)

register_setting(
    name="GC_WEB_HOME_F2_RSS_LINK",
    description=_("主站首页,论坛新手rss地址" ),
    editable=True,
    default='http://bbs.ccplay.com.cn/api.php?mod=rss&bid=101',
)


register_setting(
    name="GC_TOPICS_MASTERPIECE_SLUG",
    description=_("Topic.slug, 巨作页面，指定一个专辑(topic)展示游戏列表" ),
    editable=True,
    default='masterpiece',
    choices=topic_choices
)

register_setting(
    name="GC_TOPICS_VENDOR_SLUG",
    description=_("顶级开发商指定一个专辑(topic)展示warehouse.author列表" ),
    editable=True,
    default='spec-top-author',
    choices=topic_choices
)

register_setting(
    name="GC_TOPICS_COLLECTIONS_SLUG",
    description=_("合集的Topic.slug，指定一个专辑(topic)展示列表" ),
    editable=True,
    default='spec-choice-topic',
    choices=topic_choices
)

register_setting(
    name="GC_COMPLEX_PACKAGE_FILTER_TOPIC_SLUGS",
    description="对分类下应用列表筛选的专区列表",
    editable=True,
    default=",".join((
        'recommend',
        'basic-installed',
        'NONE'
    )),
)

register_setting(
    name="GC_RANKING_C1_RT_SLUG",
    description="榜单页面第1列的榜单类型",
    editable=True,
    choices=rankingtype_choices,
    default="main",
    )
register_setting(
    name="GC_RANKING_C2_RT_SLUG",
    description="榜单页面第2列的榜单类型",
    editable=True,
    choices=rankingtype_choices,
    default="main",
    )
register_setting(
    name="GC_RANKING_C3_RT_SLUG",
    description="榜单页面第3列的榜单类型",
    editable=True,
    choices=rankingtype_choices,
    default="main",
    )

register_setting(
    name="GC_TEMPLATE_CACHE_TIMEOUT",
    description=_("模板缓存过期时间" ),
    editable=True,
    default=3600,
)

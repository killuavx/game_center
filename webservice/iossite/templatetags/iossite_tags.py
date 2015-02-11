# -*- coding: utf-8 -*-
from django.template.base import Library
from django.core.urlresolvers import reverse

register = Library()
@register.inclusion_tag('iossite/includes/pagination_web.haml', takes_context=True)
def pagination(context, current_page, *args, **kwargs):
    return dict(
        request=context.get('request'),
        current_page=current_page
    )

@register.inclusion_tag('iossite/includes/pagination_web_ajax.html', takes_context=True)
def pagination_ajax(context, current_page, load_selector='#list', *args, **kwargs):
    return dict(
        request=context.get('request'),
        load_selector=load_selector,
        paginator_url=kwargs.get('paginator_url'),
        current_page=current_page
    )

@register.inclusion_tag('iossite/includes/package-box.haml', takes_context=True)
def package_box(context, package, *args, **kwargs):
    return dict(
        request=context.get('request'),
        package=package,
        product='web',
    )


def adv_content_url(adv, *args, **kwargs):
    if adv.get('content_url'):
        return adv.get('content_url')
    elif adv.get('content_type') == 'package':
        return reverse(viewname='package_detail', kwargs=dict(pk=adv.get('object_id', 0)))
    else:
        return None

register.assignment_tag(adv_content_url, name='adv_content_url_as')
register.simple_tag(adv_content_url)


def package_url(pkg, *args, **kwargs):
    return reverse(viewname='package_detail_default',
                   kwargs=dict(
                       pk=pkg.get('id'),
                       package_name=pkg.get('package_name'),
                   ))
register.assignment_tag(package_url, name='package_url_as')
register.simple_tag(package_url)


@register.inclusion_tag('iossite/menus/navigation.haml', takes_context=True)
def iossite_navigation(context, *args, **kwargs):
    navs = [
        dict(url='/', name='首页'),
        dict(url='/video/', name='视频',
             li_class='video-li', mark_class='mark-new', mark=True),
        dict(url='/game/', name='游戏'),
        dict(url='/application/', name='软件'),
        dict(url='/crack/', name='破解'),
        dict(url='/collections/', name='合集'),
        dict(url='/masterpiece/', name='巨作'),
        dict(url='/vendors/', name='厂商'),
        dict(url='/ranking/', name='排行',
             has_children=True,
             children=[
                 dict(url='/ranking/game/', name='游戏'),
                 dict(url='/ranking/application/', name='软件'),
             ],
        ),
        dict(url='http://bbs.ccplay.com.cn/forum-47-1.html', name='许愿'),
        dict(url='http://bbs.ccplay.com.cn/', name='论坛'),
    ]
    return dict(
        request=kwargs.get('request'),
        navs=navs,
    )

@register.filter
def navigation_active(nav_url, request):
    idx = request.path.index('/', 1)
    shortpath = request.path[0:idx+1]
    return nav_url.endswith(shortpath)


from iossite.apis import ApiFactory


@register.filter
def package_download_url(pkg):
    dw_url = 'itms-services://?action=download-manifest&url=https://ios-api.ccplay.com.cn/download/%(api_key)s/%(version_id)s.plist' % dict(api_key=ApiFactory.API_KEY, version_id=pkg['latest_version_id'])
    return dw_url

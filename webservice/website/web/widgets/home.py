# -*- coding: utf-8 -*-
from copy import deepcopy
from django.contrib.sites.models import Site
from os.path import join
from django_widgets import Widget
from toolkit.helpers import get_global_site
from website.widgets.common.promotion import BaseSingleAdvWidget, BaseMultiAdvWidget
from website.widgets.common import package as pkgwidget
from website.widgets.common import topic as tpwidget
from website.widgets.common.webspide import BaseForumThreadPanelWdiget
from website.widgets.common.author import BaseTopicAuthorPanelWidget
from website.widgets.common import filters
from . import base

__all__ = ['WebHeaderSiteListWidget',
           'WebHomeTopBannersWidget',
           'WebHomeTopicalPackageBySearchListWidget',
           'WebHomeMasterpiecePackageListWidget',
           'WebHomeLatestPackageBySearchListWidget',
           'WebSingleAdvertisementWidget',
           'WebHomeComplexPackageBySearchPanelWidget',
           'WebRankingPackageListWidget',
           'WebHomeForumHotThreadPanelWidget',
           'WebHomeForumNoviceThreadPanelWidget',
           'WebHomeVendorListWidget',
           'WebHomeCollectionListWidget',
           'WebIOSClientDownloadBox',
           'WebFooterWidget',
           ]


def get_mainsite():
    from toolkit.helpers import get_global_site, SITE_NOT_SET, SITE_ANDROID, set_global_site_id
    set_global_site_id(SITE_ANDROID)
    site = get_global_site()
    set_global_site_id(SITE_NOT_SET)
    return site


class WebHeaderSiteListWidget(Widget):

    def get_list(self):
        from toolkit import helpers
        #ios_site = Site.objects.get(pk=helpers.SITE_IOS)
        #yield dict(url="http://%s/" % ios_site.domain, name=ios_site.name, css_class='a1')
        android_site = Site.objects.get(pk=helpers.SITE_ANDROID)
        yield dict(url="http://%s/" % android_site.domain, name=android_site.name, css_class='a2')
        yield dict(url="http://ccplay.cc/product", name='产品中心', css_class='a3')

    def get_context(self, value, options):
        items = list(self.get_list())
        return dict(
            items=items
        )


class WebHomeTopBannersWidget(BaseMultiAdvWidget,
                              base.ProductPropertyWidgetMixin,
                              Widget):

    template='pages/widgets/home/banner.haml'


class WebHomeMasterpiecePackageListWidget(pkgwidget.BaseTopicalPackageListWidget,
                                          base.ProductPropertyWidgetMixin,
                                          Widget):

    per_page = 10

    template='pages/widgets/home/roll-masterpiece.haml'



class WebHomeLatestPackageListWidget(#pkgwidget.BasePackageListWidget,
                                     pkgwidget.BasePackageBySearchListWidget,
                                     base.ProductPropertyWidgetMixin,

                                     Widget):

    filter_backends = (
        filters.PackageReleasedOrderFilterBackend,
    )

    by_released = True


    def get_more_url(self):
        return '/latest/'

class WebHomeLatestPackageBySearchListWidget(pkgwidget.BasePackageBySearchListWidget,
                                             base.ProductPropertyWidgetMixin,
                                             Widget):

    filter_backends = (
        filters.SearchOrderByFilterBackend,
    )

    search_ordering = ('-released_datetime', )

    def get_more_url(self):
        return '/latest/'


class WebHomeTopicalPackageListWidget(pkgwidget.BaseTopicalPackageListWidget,
                                      base.ProductPropertyWidgetMixin,
                                      Widget):
    per_page = 8

    template = 'pages/widgets/home/roll-collections.haml'


class WebHomeTopicalPackageBySearchListWidget(pkgwidget.BasePackageBySearchListWidget,
                                              base.ProductPropertyWidgetMixin,
                                              Widget):
    topic = None
    topic_id = None
    topic_slug = None

    per_page = 8
    filter_backends = (
        filters.SearchByTopicFilterBackend,
        filters.SearchOrderByFilterBackend,
    )
    search_ordering = ('-released_datetime', )

    def setup_options(self, context, options):
        super(WebHomeTopicalPackageBySearchListWidget, self).setup_options(context, options)
        self.setup_topic(**options)

    def setup_topic(self, topic=None, topic_id=None, topic_slug=None, **kwargs):
        self.topic=topic
        self.topic_id = topic_id
        self.topic_slug = topic_slug if topic_slug != 'NONE' else topic_slug
        if self.topic:
            return
        from taxonomy.models import Topic
        if self.topic_id:
            self.topic = Topic.objects.get_cache_by(self.topic_id)
        elif self.topic_slug:
            self.topic = Topic.objects.get_cache_by_slug(get_global_site().pk,
                                                         self.topic_slug)

    def get_more_url(self):
        if self.topic:
            return self.topic.get_absolute_url_as(product=self.product,
                                                  pagetype='special')
        return 'javascript:;'

    def get_title(self):
        if self.topic:
            return self.topic.name
        else:
            return ''


class WebSingleAdvertisementWidget(BaseSingleAdvWidget,
                                   base.ProductPropertyWidgetMixin,
                                   Widget):

    template = 'pages/widgets/common/single-adv.haml'


class WebHomeComplexPackagePanelWidget(pkgwidget.BaseComplexPackageListWidget,
                                       base.ProductPropertyWidgetMixin,
                                       Widget):

    template = 'pages/widgets/home/complex-package-panel.haml'


class WebHomeComplexPackageBySearchPanelWidget(pkgwidget.BaseComplexPackageBySearchListWidget,
                                       base.ProductPropertyWidgetMixin,
                                       Widget):
    template = 'pages/widgets/home/complex-package-panel2.haml'


class WebRankingPackageListWidget(pkgwidget.BaseRankingPackageListWidget,
                                  base.ProductPropertyWidgetMixin,
                                  Widget):

    template = 'pages/widgets/common/ranking-list.haml'

    def get_title(self):
        try:
            return self.ranking.ranking_type.title
        except:
            return None

    def get_more_url(self):
        try:
            return self.ranking.get_absolute_url_as(product=self.product)
        except:
            return None


class WebHomeCollectionListWidget(tpwidget.BaseTopicListWidget,
                                  base.ProductPropertyWidgetMixin,
                                  Widget):

    template = 'pages/widgets/home/roll-collections.haml'


from website.web.widgets.collections import  WebCollectionTopicListWithSearchPackageWidget


class WebHomeCollectionPanelWidget(WebCollectionTopicListWithSearchPackageWidget):

    slug = 'spec-choice-topic'

    template = 'pages/widgets/home/collections-panel.haml'

    def get_more_url(self):
        return '/collections/'


class WebHomeForumHotThreadPanelWidget(BaseForumThreadPanelWdiget,
                                       base.ProductPropertyWidgetMixin,
                                       Widget):

    per_page = 12

    template = 'pages/widgets/home/forum-hot-list.haml'


class WebHomeForumNoviceThreadPanelWidget(BaseForumThreadPanelWdiget,
                                          base.ProductPropertyWidgetMixin,
                                          Widget):

    per_page = 12

    template = 'pages/widgets/home/forum-novice-list.haml'


class WebHomeVendorListWidget(BaseTopicAuthorPanelWidget,
                              base.ProductPropertyWidgetMixin,
                              Widget):

    template = 'pages/widgets/home/vendor-list.haml'

    title = '厂商'

    def get_more_url(self):
        return self.get_model().page_absolute_url_as(self.product)


class WebIOSClientDownloadBox(base.ProductPropertyWidgetMixin, Widget):

    template = 'pages/widgets/common/ios-downbox.html'

    client_package_name = 'com.cchelper.pc'

    def get_context(self, value, options):
        from mezzanine.conf import settings
        self.client_package_name = getattr(settings, 'GC_FOOTER_CLIENT_DOWNLOAD_PACKAGE_NAME', '')
        self.options = deepcopy(options)
        self.product = options.get('product')
        from clientapp.models import client_download_url
        download_url = client_download_url(package_name=self.client_package_name,
                                           entrytype=self.product)
        data = deepcopy(options)
        data.update(dict(
            download_url=download_url,
            product=self.product,
        ))
        return data


from django.core.urlresolvers import reverse


class WebFooterWidget(base.ProductPropertyWidgetMixin, Widget):

    template = 'pages/widgets/common/footer.haml'

    MAIN_SITE_NAME = 'ccplay.cc'

    def _static(self, url):
        from django.conf import settings
        return "%s/%s" % (settings.STATIC_URL.rstrip('/'), url.lstrip('/'))

    def _full_url(self, site, url):
        domain = site.domain
        return "http://%s/%s" % (domain, url.lstrip('/'))

    def _page_url(self, slug):
        return "http://%s/%s" % ( self.MAIN_SITE_NAME, slug.lstrip('/'))

    def get_menus_aboutus(self):
        yield dict(
            slug='about/intro',
            title='公司简介',
            full_url=self._page_url('about/intro'),
        )
        yield dict(
            slug='about/vision',
            title='发展愿景',
            full_url=self._page_url('about/vision'),
        )
        yield dict(
            slug='about/contact',
            title='联系方式',
            full_url=self._page_url('about/contact'),
        )
        yield dict(
            slug='about/joinus',
            title='诚聘英才',
            full_url=self._page_url('about/joinus'),
        )
        yield dict(
            slug='about/legal',
            title='法律声明',
            full_url=self._page_url('about/legal'),
        )
        yield dict(
            slug='about/developer',
            title='开发者平台',
            full_url='http://developer.ccplay.cc/',
        )
        yield dict(
            slug='about/anti-addiction',
            title='防沉迷系统',
            full_url=self._page_url('about/anti-addiction'),
        )
        yield dict(
            slug='about/parental-controls',
            title='家长监护工程',
            full_url=self._page_url('about/parental-controls'),
        )

    def get_menus_helpers(self):
        yield dict(
            slug='product',
            title='虫虫助手',
            cls='i-5',
            full_url=self._page_url('product'),
        )
        yield dict(
            slug='product',
            title='虫虫公会',
            cls='i-5',
            full_url=self._page_url('product/gonghui'),
        )
        #yield dict(
        #    slug='product',
        #    title='苹果PC版',
        #    cls='i-6',
        #    full_url=self._page_url('product'),
        #)

    def get_client_download_url(self):
        from toolkit import helpers
        from clientapp.models import client_download_url
        client_dw_url = client_download_url(package_name='',
                                            entrytype=self.product)
        return self._full_url(helpers.get_global_site(), client_dw_url)

    def get_product_url(self):
        uri = reverse('product')
        return self._page_url(uri)

    def get_context(self, value, options):
        from mezzanine.conf import settings
        from toolkit.helpers import current_request
        self.hostname = getattr(settings, 'GC_HOST_NAME', 'ccplay.cc')
        self.request = current_request()
        data = deepcopy(options)
        data.update(dict(
            menus_aboutus=list(self.get_menus_aboutus()),
            menus_helpers=list(self.get_menus_helpers()),
            hostname=self.hostname,
            client_download_url=self.get_client_download_url(),
            product_url=self.get_product_url(),
        ))
        return data


class WebFooterFloatBarWidget(base.ProductPropertyWidgetMixin, Widget):

    template = 'pages/widgets/common/mobile_floatbar.haml'

    def get_client_download_url(self):
        from toolkit import helpers
        from clientapp.models import client_download_url
        client_dw_url = client_download_url(package_name='',
                                            entrytype=self.product)
        return self._full_url(helpers.get_global_site(), client_dw_url)

    def _full_url(self, site, url):
        domain = site.domain
        return "http://%s/%s" % (domain, url.lstrip('/'))

    def get_context(self, value, options):
        from toolkit.helpers import current_request
        self.request = current_request()
        data = deepcopy(options)
        data.update(dict(
            client_download_url=self.get_client_download_url()
        ))
        return data

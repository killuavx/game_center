# -*- coding: utf-8 -*-
from copy import deepcopy
from django.contrib.sites.models import Site
from os.path import join
from django_widgets import Widget
from website.widgets.common.promotion import BaseSingleAdvWidget, BaseMultiAdvWidget
from website.widgets.common import package as pkgwidget
from website.widgets.common import topic as tpwidget
from website.widgets.common.webspide import BaseForumThreadPanelWdiget
from website.widgets.common.author import BaseTopicAuthorPanelWidget
from website.widgets.common import filters
from . import base

__all__ = ['WebHeaderSiteListWidget',
           'WebHomeTopBannersWidget',
           'WebHomeTopicalPackageListWidget',
           'WebHomeMasterpiecePackageListWidget',
           'WebHomeLatestPackageListWidget',
           'WebSingleAdvertisementWidget',
           'WebHomeComplexPackagePanelWidget',
           'WebRankingPackageListWidget',
           'WebHomeForumHotThreadPanelWidget',
           'WebHomeForumNoviceThreadPanelWidget',
           'WebHomeVendorListWidget',
           'WebHomeCollectionListWidget',
           'WebIOSClientDownloadBox',
           'WebFooterWidget',
           ]


class WebHeaderSiteListWidget(Widget):

    def get_list(self):
        from toolkit import helpers
        #site = Site.objects.get(pk=helpers.SITE_IOS)
        #yield dict(url="http://%s/" % site.domain, name=site.name, css_class='a1')
        #site = Site.objects.get(pk=helpers.SITE_ANDROID)
        #yield dict(url="http://%s/" % site.domain, name=site.name, css_class='a2')
        yield dict(url="/static/cc_web/html/a-down.html", name='虫虫助手', css_class='a3')

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



class WebHomeLatestPackageListWidget(pkgwidget.BasePackageListWidget,
                                     base.ProductPropertyWidgetMixin,
                                     Widget):

    filter_backends = (
        filters.PackageReleasedOrderFilterBackend,
    )

    by_released = True


    def get_more_url(self):
        return '/latest/'


class WebHomeTopicalPackageListWidget(pkgwidget.BaseTopicalPackageListWidget,
                                      base.ProductPropertyWidgetMixin,
                                      Widget):
    per_page = 8

    template = 'pages/widgets/home/roll-collections.haml'


class WebSingleAdvertisementWidget(BaseSingleAdvWidget,
                                   base.ProductPropertyWidgetMixin,
                                   Widget):

    template = 'pages/widgets/common/single-adv.haml'


class WebHomeComplexPackagePanelWidget(pkgwidget.BaseComplexPackageListWidget,
                                       base.ProductPropertyWidgetMixin,
                                       Widget):

    template = 'pages/widgets/home/complex-package-panel.haml'


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
        from django.core.urlresolvers import reverse
        self.options = deepcopy(options)
        self.product = options.get('product')
        download_url = reverse('clientapp-latest_download',
                               kwargs=dict(package_name=self.client_package_name))
        data = deepcopy(options)
        data.update(dict(
            download_url=download_url,
            product=self.product,
        ))
        return data


class WebFooterWidget(base.ProductPropertyWidgetMixin, Widget):

    template = 'pages/widgets/common/footer.haml'

    def _static(self, url):
        from django.conf import settings
        return "%s/%s" % (settings.STATIC_URL, url.lstrip('/'))

    def _full_url(self, site, url):
        domain = site.domain
        return "http://%s/%s" % (domain, url.lstrip('/'))

    def get_menus_aboutus(self):
        yield dict(
            slug='intro',
            title='公司简介',
            full_url=self._static('ios_web/html/about.html'),
        )
        yield dict(
            slug='vision',
            title='发展愿景',
            full_url=self._static('ios_web/html/vision.html'),
        )
        yield dict(
            slug='contact',
            title='联系方式',
            full_url=self._static('ios_web/html/contact.html'),
        )
        yield dict(
            slug='job',
            title='诚聘英才',
            full_url=self._static('ios_web/html/job.html'),
        )

    def get_menus_helpers(self):
        yield dict(
            slug='cchelpers/android',
            title='Android版',
            cls='i-5',
            full_url=self._static('cc_web/html/a-download.html'),
        )

    def get_client_download_url(self):
        from django.core.urlresolvers import reverse
        client_dw_url = reverse('clientapp-latest_download',
                                kwargs=dict(package_name=''))
        from toolkit import helpers
        return self._full_url(helpers.get_global_site(), client_dw_url)

    def get_context(self, value, options):
        from mezzanine.conf import settings
        from toolkit.helpers import current_request
        self.hostname = getattr(settings, 'GC_HOST_NAME', 'www.ccplay.com.cn')
        self.request = current_request()
        data = deepcopy(options)
        data.update(dict(
            menus_aboutus=list(self.get_menus_aboutus()),
            menus_helpers=list(self.get_menus_helpers()),
            hostname=self.hostname,
            client_download_url=self.get_client_download_url(),
        ))
        return data




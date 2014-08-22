# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.filters import BaseWidgetFilterBackend, PackageByCategorySearcherFilter
from website.widgets.common import package as pkgwidget
from .base import ProductPropertyWidgetMixin
from haystack.utils import get_identifier
from haystack.constants import ID

__all__ = ['WebPackageRelatedBySearchListWidget']

class ExcludePackageSearcherFilterBackend(BaseWidgetFilterBackend):

    exclude_package_param = 'package'

    def filter_queryset(self, request, queryset, widget):
        package = getattr(widget, self.exclude_package_param, None)
        if package:
            return queryset.exclude(**{ID:get_identifier(package)})
        return queryset


class WebPackageRelatedListWidget(pkgwidget.BasePackageSearchListWidget,
                                  ProductPropertyWidgetMixin,
                                  Widget):

    search_fields = ('tags_text', 'categories', 'title')

    class WebPackageByCategorySearcherFilter(PackageByCategorySearcherFilter):

        hit_category = True

        cat_param = 'cat'

    filter_backends = [
        WebPackageByCategorySearcherFilter,
        ExcludePackageSearcherFilterBackend
    ]

    def get_search_terms(self, options):
        tags = list(set(self.package.tags_text.split() + self.version.tags_text.split()))
        return tags

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        self.package = options.get('package')
        self.version = options.get('version')
        if not self.package and not self.version:
            raise ValueError

        if not self.version:
            self.version = self.package.versions.latest_published()
        if not self.package:
            self.package = self.version.package

        self.options = options

        if self.package.main_category:
            self.options['cat'] = self.package.main_category.get_root()
        else:
            self.options['cat'] = None
        return super(WebPackageRelatedListWidget, self).get_context(value=value,
                                                                    options=options,
                                                                    context=context,
                                                                    pagination=pagination)


class WebPackageRelatedBySearchListWidget(pkgwidget.BasePackageRelatedBySearchListWidget,
                                          ProductPropertyWidgetMixin,
                                          Widget):
    pass

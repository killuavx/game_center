# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.author import BaseTopicAuthorPanelWidget
from website.widgets.common.package import BasePackageListWidget
from website.widgets.common.base import BaseWidgetFilterBackend, FilterWidgetMixin, OrderingFitler

__all__ = ['PCVendorNavListWidget', 'PCVendorPackageListWidget']


class PCVendorCurrentAuthorMixin(object):

    author = None

    def set_current_author(self, items, author, context):
        if author:
            self.author = author
        else:
            self.author = items[0]

        for author in items:
            author.is_current = False
            if author.pk == self.author.pk:
                author.is_current = True
        context['current_author'] = self.author

    def get_current_author(self, context):
        return context['current_author']


class PCVendorNavListWidget(PCVendorCurrentAuthorMixin,
                            BaseTopicAuthorPanelWidget,
                            Widget):

    template = None

    author = None

    def get_context(self, value=None, options=dict(), context=None):
        data = super(PCVendorNavListWidget, self).get_context(value=value,
                                                              options=options,
                                                              context=context)
        self.set_current_author(data['items'],
                                author=options.get('author'),
                                context=context)
        return data


class AuthorPackageWidgetFilter(BaseWidgetFilterBackend):

    author_param = 'author'

    def filter_queryset(self, request, queryset, widget):
        if hasattr(widget, self.author_param):
            author = getattr(widget, self.author_param)
            return queryset.filter(author=author)
        return queryset


class PCVendorPackageListWidget(PCVendorCurrentAuthorMixin,
                                BasePackageListWidget,
                                Widget):

    filter_backends = (AuthorPackageWidgetFilter,
                       OrderingFitler)

    template = None

    author = None

    ordering = ('-released_datetime', )

    per_page = 18

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        self.author = options.get('author')
        if not self.author:
            self.author = self.get_current_author(context)
        return super(PCVendorPackageListWidget, self).get_context(value=value,
                                                                  options=options,
                                                                  context=context,
                                                                  pagination=pagination)


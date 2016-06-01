# -*- coding: utf-8 -*-
import six
from copy import deepcopy

class PaginatorPageMixin(object):

    list_page_var = 'list_page'

    per_page = 10

    def set_list_page(self, list_page, options, context):
        list_page_var = options.get('list_page_var') \
            if options.get('list_page_var') else self.list_page_var
        context[list_page_var] = list_page

    def get_list_page(self, options, context):
        list_page_var = options.get('list_page_var') \
            if options.get('list_page_var') else self.list_page_var
        return list_page_var, context.get(list_page_var)

    def get_paginator_vars(self, options):
        if 'max_items' in options:
            per_page = options.get('max_items') if options.get('max_items') else self.per_page
        elif 'per_page' in options:
            per_page = options.get('per_page') if options.get('per_page') else self.per_page
        else:
            per_page = self.per_page

        if str(options.get('page')).isnumeric():
            page = int(options.get('page'))
        elif str(options.get('page_num')).isnumeric():
            page = int(options.get('page_num'))
        else:
            page = 1

        return per_page, page


class BaseListWidget(PaginatorPageMixin):

    more_url = None

    title = None

    max_paging_links = 10

    request = None

    def get_title(self):
        return self.title

    def get_more_url(self):
        return self.more_url

    def get_list(self):
        return list()

    def setup_options(self, context, options):
        self.title = options.get('title', self.title)
        self.request = context.get('request')
        self.product = options.get('product')
        self.context = context
        self.options = options
        if options.get('template_name'):
            self.template = options.get('template_name')

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        self.setup_options(context, options)
        from mezzanine.utils.views import paginate
        per_page, page = self.get_paginator_vars(options)
        items = paginate(self.get_list(),
                         page_num=page,
                         per_page=per_page,
                         max_paging_links=self.max_paging_links)
        data = deepcopy(options)
        data.update(
            title=self.get_title(),
            more_url=self.get_more_url(),
            items=items,
            product=self.product,
            request=self.request,
            paginator=items.paginator,
        )
        self.set_list_page(items, options, context)
        return data

    def render(self, context, value=None, attrs=None):
        if attrs.get('template', None):
            self.template_instance = None
            self.template = attrs.get('template')
        return super(BaseListWidget, self).render(context, value=value, attrs=attrs)


class BaseWidgetFilterBackend(object):

    def filter_queryset(self, request, queryset, widget):
        """
        Return a filtered queryset.
        """
        raise NotImplementedError(".filter_queryset() must be overridden.")


class FilterWidgetMixin(object):

    filter_backends = ()

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.

        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        filter_backends = self.filter_backends or []
        for backend in filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class OrderingFitler(BaseWidgetFilterBackend):

    ordering_param = 'ordering'

    def get_ordering(self, widget):
        ordering = getattr(widget, self.ordering_param, None)
        if isinstance(ordering, six.string_types):
            return (ordering,)
        return ordering

    def filter_queryset(self, request, queryset, widget):
        ordering = self.get_ordering(widget)
        if ordering:
            return queryset.order_by(*ordering)

        return queryset
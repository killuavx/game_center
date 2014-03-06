# -*- coding: utf-8 -*-
from django_widgets import Widget
from django.core.paginator import Paginator


class PaginatorPageMixin(object):

    list_page_var = 'list_page'

    def set_list_page(self, list_page, options, context):
        list_page_var = options.get('list_page_var') \
            if options.get('list_page_var') else self.list_page_var
        context[list_page_var] = list_page

    def get_list_page(self, options, context):
        list_page_var = options.get('list_page_var') \
            if options.get('list_page_var') else self.list_page_var
        return list_page_var, context.get(list_page_var)


class BaseListWidget(PaginatorPageMixin, Widget):

    more_url = None

    title = None

    per_page = 10

    def get_more_url(self):
        return self.more_url

    def get_list(self):
        return list()

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

    def get_context(self, value=None, options=dict(), context=None):
        per_page, page = self.get_paginator_vars(options)
        paginator = Paginator(self.get_list(), per_page=per_page)
        items = paginator.page(page)
        options.update(
            title=options.get('title', self.title),
            more_url=self.get_more_url(),
            items=items,
            page=page,
            per_page=per_page
        )
        self.set_list_page(items, options, context)
        return options



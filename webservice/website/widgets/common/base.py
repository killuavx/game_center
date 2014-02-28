# -*- coding: utf-8 -*-
from django_widgets import Widget
from django.core.paginator import Paginator


class BaseListWidget(Widget):

    more_url = None

    title = None

    per_page = 10

    def get_more_url(self):
        return self.more_url

    def get_list(self):
        return list()

    def get_context(self, value=None, options=dict(), context=None):
        per_page = None
        if 'max_items' in options:
            per_page = options.get('max_items') if options.get('max_items') else self.per_page
        elif 'per_page' in options:
            per_page = options.get('per_page') if options.get('per_page') else self.per_page
        else:
            per_page = self.per_page

        page = options.get('page') if options.get('page') else 1
        paginator = Paginator(self.get_list(), per_page=per_page)
        items = paginator.page(page)
        options.update(
            title=options.get('title', self.title),
            more_url=self.get_more_url(),
            items=items,
            page=page,
            per_page=per_page
        )
        return options

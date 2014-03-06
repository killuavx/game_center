# -*- coding: utf-8 -*-
from django_widgets import Widget
from .base import PaginatorPageMixin


class BasePaginatorWidget(PaginatorPageMixin, object):

    per_page = 10

    def get_context(self, value=None, options=dict(), context=dict()):
        page = options.get('page') if options.get('page') else 1
        list_page_var, list_page = self.get_list_page(options, context)
        options.update({
            'list_page': list_page,
            'page': page
        })
        return options


class PaginatorPrevNextWidget(BasePaginatorWidget, Widget):

    template = 'pages/widgets/common/paginator-prevnext.haml'

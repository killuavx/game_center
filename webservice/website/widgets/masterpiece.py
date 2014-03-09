# -*- coding: utf-8 -*-
from django.core.paginator import EmptyPage
from django.http import Http404
from .common.topic import BaseTopicPackageListWidget, BaseTopicInformationWidget


class MasterpieceInformationWidget(BaseTopicInformationWidget):

    template = 'pages/widgets/masterpiece/information.haml'


class MasterpiecePackageListWidget(BaseTopicPackageListWidget):

    per_page = 8

    template = 'pages/widgets/masterpiece/package-list.haml'

    def get_context(self, value=None, options=dict(), context=None):
        try:
            return super(MasterpiecePackageListWidget, self).get_context(value,
                                                                         options,
                                                                         context)
        except EmptyPage:
            raise Http404()

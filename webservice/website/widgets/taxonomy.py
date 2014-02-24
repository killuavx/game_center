# -*- coding: utf-8 -*-
from django_widgets import Widget


class TopicBannerListWidget(Widget):

    template = 'website/widgets/taxonomy/topic-banner.haml'

    def get_context(self, value=None, options=dict(), context=None):
        options.update(
            id=options.get('id'),
            max_items=options.get('max_items', 6),
            items=options.get('items', list()),
            )
        return options

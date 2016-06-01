# -*- coding: utf-8 -*-

class BasePostWidget(object):

    more_url = None

    def get_more_url(self):
        return self.more_url

    def get_list(self, category_slug=None, max_items=5):
        from mezzanine.blog.models import BlogPost
        queryset = BlogPost.objects.published()
        if category_slug is not None:
            queryset = queryset.filter(categories__contains=category_slug)
        return queryset[0:max_items]

    def get_context(self, value=None, options=dict(), context=None):
        max_items = options.get('max_items', 5)
        options.update(
            more_url=self.get_more_url(),
            max_items=max_items,
            items=self.get_list(category_slug=options.get('category'),
                                max_items=max_items)
        )
        return options



# -*- coding: utf-8 -*-
from feedparser import parse
from website.widgets.common.base import BaseListWidget


class BaseForumThreadPanelWdiget(BaseListWidget):

    rss_link = None

    def get_rss_content(self):
        if not hasattr(self, '_rss'):
            try:
                self._rss = parse(self.rss_link)
            except:
                self._rss = None
        return self._rss

    def get_more_url(self):
        try:
            return self.get_rss_content()['feed']['link']
        except:
            return None

    def get_title(self):
        try:
            return self.get_rss_content()['feed']['title']
        except:
            return None

    def get_list(self):
        try:
            posts = self.get_rss_content()['entries']
        except:
            return list()
        items = []
        for post in posts:
            items.append(dict(
                title=post.title,
                url=post.link,
                summary=post.summary,
                avatar_url=post.avatar,
                replies_count=post.replies,
                views_count=post.views,
                category=post.category,
                category_url=post.categorylink,
                pub_date=post.published
            ))
        return items

    def get_context(self, value=None, options=dict(), context=None, *kwargs):
        self.rss_link = options.get('rss_link')
        return super(BaseForumThreadPanelWdiget, self).get_context(value=value,
                                                            options=options,
                                                            context=context
                                                            )


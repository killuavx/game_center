# -*- coding: utf-8 -*-
from dateutil import parser
from feedparser import parse

class BaseForumThreadPanelWdiget(object):

    rss_link = 'http://bbs.ccplay.com.cn/api.php?mod=rss&bid=45'

    more_url = 'http://bbs.ccplay.com.cn/'

    def get_more_url(self):
        return self.more_url

    def get_list(self):
        posts = parse(self.rss_link)['entries']
        items = []
        for post in posts:
            items.append(dict(
                title=post.title,
                url=post.link,
                category=post.category,
                category_url=post.categorylink,
                pub_date=post.published
            ))
        return items

    def get_context(self, value=None, options=dict(), context=None):
        items = self.get_list()
        max_items = options.get('max_items', 5)
        options.update(
            title=options.get('title'),
            more_url=self.get_more_url(),
            items=options.get('items', list(items[0:max_items])),
            max_items=max_items,
            )
        return options

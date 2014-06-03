# -*- coding: utf-8 -*-
from feedparser import parse
from website.widgets.common.base import BaseListWidget


class BaseForumThreadPanelWdiget(BaseListWidget):

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

    def get_context(self, value=None, options=dict(), context=None, *kwargs):
        return super(BaseForumThreadPanelWdiget, self).get_context(value=value,
                                                            options=options,
                                                            context=context
                                                            )


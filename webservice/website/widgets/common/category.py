# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from taxonomy.models import Category, Topic, TopicalItem
from warehouse.models import Author
import re


class BaseCategoryPackageListWidget(object):

    slugs = ('crack-game',
             'big-game',
             'cn-game',
             'online-game',
             'standalone-relaxation-game',
             'standalone-action-game',
    )

    def get_more_url(self):
        return reverse('mezzanine.pages.views.page', kwargs=dict(slug='categories'))

    def get_package_list_by(self, category):
        return category.packages.published()

    def get_category(self, slug):
        return Category.objects.get(slug=slug)

    def convert_slugs_from_args(self, slugs):
        if isinstance(slugs, str):
            p = re.compile('[^,\s]+')
            slugs = re.findall(p, slugs)

        return slugs

    def get_context(self, value=None, options=dict(), context=None):
        slugs = self.convert_slugs_from_args(options.get('slugs', self.slugs))
        max_items = options.get('max_items', 5)
        group_items = list()
        for slug in slugs:
            try:
                category = self.get_category(slug=slug)
            except Category.DoesNotExist:
                continue
            packages = self.get_package_list_by(category)
            group_items.append((category, packages[0:max_items]))

        options.update(
            title=options.get('title'),
            more_url=self.get_more_url(),
            group_items=group_items,
            max_items=max_items,
            )
        return options


class BaseTopicAuthorPackageListWidget(object):

    slug = 'spec-top-author'

    def get_package_list_by(self, author):
        return author.packages.by_published_order(newest=True)

    def get_topic_authors(self):
        topic = Topic.objects.get(slug=self.slug)
        return TopicalItem.objects\
            .get_items_by_topic(topic=topic, item_model=Author)\
            .published()

    def get_context(self, value=None, options=dict(), context=None):
        self.slug = options.get('slug', self.slug)
        max_items = options.get('max_items', 36)
        max_developers = options.get('max_developers', 10)
        group_items = list()
        authors = self.get_topic_authors()[0:max_developers]
        for author in authors:
            packages = self.get_package_list_by(author=author)
            group_items.append((author, packages[0:max_items]))

        options.update(dict(
            group_items=group_items,
            max_items=max_items,
            max_developers=max_developers
        ))
        return options

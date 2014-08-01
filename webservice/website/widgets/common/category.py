# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from taxonomy.models import Category, Topic, TopicalItem
from warehouse.models import Author
from toolkit.memoizes import orms_memoize, memoize
from toolkit.helpers import get_global_site


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
        return author.packages.published().by_released_order(newest=True)

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


class BaseCategorySelectorWidget(object):

    default_timeout = 86400 * 7

    packages_zero_ignore = True

    @orms_memoize(timeout=default_timeout)
    def get_cache_category_selectlist(self, cat_id):
        category = Category.objects.get_cache_category(cat_id)
        catlist = list()
        for cat in category.get_leafnodes():
            cat.affiliated_packages_count = cat.get_affiliated_packages() \
                .published().count()
            if cat.affiliated_packages_count == 0 and self.packages_zero_ignore:
                continue
            catlist.append(cat)
        category.affiliated_packages_count = category.get_affiliated_packages() \
            .published().count()
        catlist.insert(0, category)
        return catlist

    def get_category_selectlist(self, cat_id):
        cats = self.get_cache_category_selectlist(cat_id)
        return cats

    @memoize(timeout=default_timeout)
    def get_second_selectlist(self, site_id=None, slugs=None):
        #slugs = slugs + ['ZH', 'EN']
        result = []
        for s in slugs:
            params = dict(topic=None, lang=None)
            if s == 'NONE':
                result.append(dict(params=params, name='最新发布'))
            elif s in ('ZH', 'EN'):
                params['lang'] = s
                if s == 'ZH':
                    result.append(dict(params=params, name='中文'))
                if s == 'EN':
                    result.append(dict(params=params, name='英文'))
            else:
                try:
                    topic = Topic.objects.get(pk=s)
                except Topic.DoesNotExist:
                    continue
                params['topic'] = topic.pk
                result.append(dict(params=params, name=topic.name))
        return result

    def get_context(self, value, options):
        self.product = options.get('product')
        root_category = options.get('root_category')
        if isinstance(root_category, int):
            cat_id = root_category
        else:
            cat_id = root_category.pk
        category_selectlist = self.get_category_selectlist(cat_id)

        from mezzanine.conf import settings
        slug_text = getattr(settings, 'GC_COMPLEX_PACKAGE_FILTER_TOPIC_SLUGS')
        slugs = list(filter(lambda x: x, slug_text.split(',')))
        second_selectlist = self.get_second_selectlist(get_global_site().pk, slugs)

        return dict(
            product=self.product,
            category_selectlist=category_selectlist,
            second_selectlist=second_selectlist,
            )


# -*- coding: utf-8 -*-
from . import base
from . import filters
from . import package as pkgwidget


class BaseTopicAuthorPanelWidget(base.BaseListWidget):

    slug = 'spec-top-author'

    def _get_default_slug(self):
        from mezzanine.conf import settings
        return getattr(settings, 'GC_TOPICS_VENDOR_SLUG', 'spec-top-author')

    def get_more_url(self):
        return ''

    def get_model(self):
        from warehouse.models import Author
        return Author

    def get_list(self):
        from taxonomy.models import Topic, TopicalItem
        slug = self.slug
        model = self.get_model()
        try:
            topic = Topic.objects.published().get(slug=slug)
            return TopicalItem.objects.get_items_by_topic(topic=topic,
                                                          item_model=model)
        except (Topic.DoesNotExist, model.DoesNotExist) as e:
            return model.objects.none()

    def get_context(self, value=None, options=dict(), context=None):
        self.slug = options.get('slug', self._get_default_slug())
        options.update(dict(
            slug=self.slug,
        ))
        return super(BaseTopicAuthorPanelWidget, self)\
            .get_context(value=value, options=options, context=context)


class BaseVendorCurrentAuthorMixin(object):

    author = None

    def set_current_author(self, items, author, context):
        if author:
            self.author = author
        else:
            self.author = items[0]

        for author in items:
            author.is_current = False
            if author.pk == self.author.pk:
                author.is_current = True
        context['current_author'] = self.author

    def get_current_author(self, context):
        return context['current_author']


class BaseVendorNavListWidget(BaseVendorCurrentAuthorMixin,
                              BaseTopicAuthorPanelWidget):
    template = None

    author = None

    def get_context(self, value=None, options=dict(), context=None):
        data = super(BaseVendorNavListWidget, self).get_context(value=value,
                                                              options=options,
                                                              context=context)
        self.set_current_author(data['items'],
                                author=options.get('author'),
                                context=context)
        return data


class BaseVendorPackageListWidget(BaseVendorCurrentAuthorMixin,
                                  pkgwidget.BasePackageListWidget):

    filter_backends = (filters.AuthorPackageWidgetFilter,
                       filters.PackageReleasedOrderFilterBackend)

    template = None

    author = None

    by_released = True

    per_page = 18

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        self.author = options.get('author')
        if not self.author:
            self.author = self.get_current_author(context)
        return super(BaseVendorPackageListWidget, self)\
            .get_context(value=value,
                         options=options,
                         context=context,
                         pagination=pagination)

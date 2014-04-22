# -*- coding: utf-8 -*-
from django.http import Http404
from django_widgets import Widget
from taxonomy.models import Category
from warehouse.models import Package
from django.core.paginator import Paginator, EmptyPage
from . import base



ORDERINGS = {'release': 'released_datetime', 'hot': 'download_count'}

class CategoryWidgetMixin(object):

    def configure_settings(self):
        from mezzanine.conf import settings
        self.slug = settings.GC_CATEGORIES_DEFAULT_SLUG


class CategoryTopMenuWidget(CategoryWidgetMixin, Widget):

    template = 'pages/widgets/categories/top-menu.haml'

    slug = 'big-game'

    root_slug = 'game'

    application_slug = 'application'

    ordering = 'release'

    def get_category(self, slug):
        category = Category.objects.get(slug=slug)
        return category

    def get_flat_categories(self):
        root = Category.objects.get(slug=self.root_slug)
        leafnodes = list(root.get_leafnodes().published().showed())
        application = Category.objects.get(slug=self.application_slug)
        leafnodes.append(application)
        return leafnodes

    def get_context(self, value=None, options=dict(), context=None):
        self.configure_settings()
        slug = options.get('slug') if options.get('slug') else self.slug
        ordering = options.get('ordering') if options.get('ordering') else self.ordering
        try:
            category = self.get_category(slug=slug)
        except:
            raise Http404()
        flat_categories = self.get_flat_categories()

        options.update(dict(
            slug=self.slug,
            category=category,
            flat_categories=flat_categories,
            ordering=ordering
        ))
        return options


class CategoryPackageListWidget(CategoryWidgetMixin, base.BaseListWidget):

    template = 'pages/widgets/categories/package-list.haml'

    slug = 'big-game'

    ordering = 'release'

    per_page = 36

    def get_list(self):
        try:
            category = Category.objects.get(slug=self.slug)
        except Category.DoesNotExist:
            raise Http404()
        qs = category.packages.published()

        return qs.order_by('-%s' % self.order_field)

    def get_ordering_field(self, ordering):
        if ordering not in ORDERINGS:
            ordering = 'release'
        order_field = ORDERINGS.get(ordering)
        return order_field

    def get_context(self, value=None, options=dict(), context=None):
        self.configure_settings()
        self.slug = options.get('slug') if options.get('slug') else self.slug
        self.ordering = options.get('ordering') if options.get('ordering') else self.ordering
        self.order_field = self.get_ordering_field(self.ordering)
        try:
            return super(CategoryPackageListWidget, self)\
                .get_context(value=value, options=options, context=context)
        except EmptyPage as e:
            raise Http404()

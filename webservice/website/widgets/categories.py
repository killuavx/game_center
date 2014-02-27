# -*- coding: utf-8 -*-
from django.http import Http404
from django_widgets import Widget
from taxonomy.models import Category
from warehouse.models import Package
from django.core.paginator import Paginator, EmptyPage


ORDERINGS = {'release': 'released_datetime', 'hot': 'download_count'}


class CategoryTopMenuWidget(Widget):

    template = 'pages/widgets/categories/top-menu.haml'

    slug = 'big-game'

    root_slug = 'game'

    application_slug = 'application'

    orderings = ORDERINGS

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
        slug = options.get('slug') if options.get('slug') else self.slug
        ordering = options.get('ordering') if options.get('ordering') else self.ordering
        print(options)
        print(ordering)
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


class CategoryPackageListWidget(Widget):

    template = 'pages/widgets/categories/package-list.haml'

    slug = 'big-game'

    orderings = ORDERINGS

    ordering = 'release'

    per_page_items = 36

    def get_list(self, slug, order_field):
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise Http404()
        qs = category.packages.published()

        return qs.order_by('-%s' % order_field)

    def get_ordering_field(self, ordering):
        if ordering not in self.orderings:
            ordering = 'release'
        order_field = self.orderings.get(ordering)
        return order_field

    def get_context(self, value=None, options=dict(), context=None):
        slug = options.get('slug') if options.get('slug') else self.slug
        ordering = options.get('ordering') if options.get('ordering') else self.ordering
        packages = self.get_list(slug=slug, order_field=self.get_ordering_field(ordering))

        try:
            per_page_items = int(options.get('per_page_items', self.per_page_items))
        except:
            per_page_items = 24

        try:
            page = int(options.get('page'))
        except:
            page = 1

        paginator = Paginator(packages, per_page_items)
        try:
            options.update(dict(
                packages=paginator.page(page),
                page=page,
                ordering=ordering
            ))
        except EmptyPage:
            raise Http404()
        return options

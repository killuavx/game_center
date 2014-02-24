# -*- coding: utf-8 -*-
from django_widgets import Widget
from warehouse.models import PackageVersion
from mobapi.warehouse.serializers.packageversion import PackageVersionDetailSerializer


class PackageListSideWidget(Widget):

    template = 'website/widgets/package/list-style1-widget.haml'

    def get_context(self, value=None, options=dict(), context=None):
        options.update(
            id=options.get('id'),
            title=options.get('title', '--no-title--'),
            more_url=options.get('more_url', None),
            max_items=options.get('max_items', 5),
            items=options.get('items', list()),
        )
        return options


class RecentlyPackageListSideWidget(Widget):

    template = 'website/widgets/package/list-style1-widget.haml'

    def get_context(self, value=None, options=dict(), context=None):
        max_items = int(options.get('max_items', 5))
        items = PackageVersion.objects.published().all()[0:max_items]
        items_serializer = PackageVersionDetailSerializer(items, many=True)
        options.update(
            id=options.get('id'),
            title=options.get('title', '--no-title--'),
            more_url=options.get('more_url', None),
            max_items=max_items,
            items=items_serializer.data
            )
        return options


class NewCrackPackageListSideWidget(Widget):

    template = 'website/widgets/package/list-style2-widget.haml'

    def get_context(self, value=None, options=dict(), context=None):
        max_items = int(options.get('max_items', 5))
        items = PackageVersion.objects.published().all()[0:max_items]
        items_serializer = PackageVersionDetailSerializer(items, many=True)
        options.update(
            id=options.get('id'),
            title=options.get('title', '--no-title--'),
            more_url=options.get('more_url', None),
            max_items=max_items,
            items=items_serializer.data
        )
        return options




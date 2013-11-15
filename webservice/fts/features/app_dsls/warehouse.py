# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy as reverse
from django.utils.timezone import now, timedelta
from fts.helpers import add_model_objects, SubFile, create_author, guid
from warehouse.models import Package, PackageVersion
from taxonomy.models import Category
from os.path import join
from should_dsl import should, should_not
from django.test.testcases import override_settings
from django.db.models.query import Q


def to_package_categories(package, text):
    text = text.strip()
    cats = text.split(',')
    for cat in cats:
        name_or_slug = cat.strip()
        try:
            c = Category.objects.get(Q(slug=name_or_slug) | Q(name=name_or_slug))
        except Category.DoesNotExist:
            raise Category.DoesNotExist("name or slug: %s" % name_or_slug)
        package.categories.add(c)


def to_package_tags(package, text):
    package.tags_text = text


class WarehouseBaseDSL(object):

    @classmethod
    def setup(cls, context):
        pass

    @classmethod
    def teardown(cls, context):
        pass

    @classmethod
    def create_author_without_ui(cls, context, **kwargs):
        name = guid()[:10]
        kwargs.setdefault('email', '%s@testcase.com' % name)
        kwargs.setdefault('name', name)
        return create_author(**kwargs)

    @classmethod
    def get_package_detail_url(cls, context, package):
        url = reverse('package-detail', kwargs=dict(pk=package.pk))
        return join(context.base_url, url)

    @classmethod
    def receive_result(cls, context):
        return context.world.get('content_json')

    @classmethod
    @override_settings(PACKAGE_FILE_PARSE_OPTS=dict(
        package_version_parser_class=None,
        package_version_parse_handle_class=None
    ))
    def create_package_without_ui(cls, context, **kwargs):
        """
        :param context:
        :param kwargs:
            :title:
            :package_name:
            :categories: "," separates categories
            :tags: "," separates tags
            :version_name:
            :version_code:
            :status
        """
        yesterday = now() - timedelta(days=1)
        released_datetime = kwargs.get('released_datetime', yesterday)
        package_name = kwargs.get('package_name')
        try:
            package = Package.objects.get(package_name=package_name)
        except Package.DoesNotExist:
            package = Package.objects.create(
                title=kwargs.get('title'),
                package_name=kwargs.get('package_name'),
                author=cls.create_author_without_ui(context),
                status=kwargs.get('status'),
                released_datetime=released_datetime,
            )

        to_package_categories(package, kwargs.get('categories'))
        to_package_tags(package, kwargs.get('tags'))
        package.save()

        package_version = PackageVersion.objects.create(
            package=package,
            version_code=kwargs.get('version_code'),
            version_name=kwargs.get('version_name'),
            status=kwargs.get('status'),
            released_datetime=released_datetime,
            icon=SubFile.icon(),
            cover=SubFile.cover(),
            download=SubFile.package()
        )

        if not context.world.get('packages'):
            context.world['packages'] = dict()

        add_model_objects(package)
        context.world.get('packages').update(dict(
            package_name=package.package_name
        ))

    @classmethod
    def visit_package_detail(cls, context, package):
        url = cls.get_package_detail_url(context, package)
        full_url = "%s%s" % (context.base_url, url)
        context.browser.visit(full_url)

    @classmethod
    def follow_package_detail_above(cls, context, field):
        related_url = cls.receive_result(context).get(field)
        related_url |should_not| be(None)
        context.browser.visit(related_url)

    @classmethod
    def visit_comment_list(cls, context, package):
        from mobapi.serializers import PackageDetailSerializer
        serializer = PackageDetailSerializer(package)
        comment_url = serializer.data.get('comments_url')
        context.browser.visit(comment_url)


class WarehouseUsingNoUIClientDSL(WarehouseBaseDSL):

    pass


class WarehouseUsingBrowserDSL(WarehouseBaseDSL):

    pass


def factory_dsl(context):
    if 'browser' in context.tags:
        return WarehouseUsingBrowserDSL

    return WarehouseUsingNoUIClientDSL


def setup(context):
    factory_dsl(context).setup(context)


def teardown(context):
    factory_dsl(context).teardown(context)

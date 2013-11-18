# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy as reverse
from django.utils.timezone import now, timedelta
from fts.helpers import (add_model_objects,
                         clear_data,
                         SubFile,
                         create_author,
                         guid)
from warehouse.models import Package, PackageVersion
from should_dsl import should, should_not
from django.test.testcases import override_settings

def to_package_categories(package, text):
    from taxonomy.models import Category
    from django.db.models.query import Q
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
        clear_data()

    @classmethod
    def create_author_without_ui(cls, context, **kwargs):
        name = guid()[:10]
        kwargs.setdefault('email', '%s@testcase.com' % name)
        kwargs.setdefault('name', name)
        return create_author(**kwargs)

    @classmethod
    def get_package_detail_url(cls, context, package):
        url = reverse('package-detail', kwargs=dict(pk=package.pk))
        return "%s%s" % (context.base_url, url)

    @classmethod
    def receive_result(cls, context):
        return context.world.get('content_json')

    @classmethod
    def create_package_without_ui(cls, context, with_version=True, **kwargs):
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

        default_name_or_title = "com.fts.%s" % guid()
        try:
            _kw = cls._dict_package_name_or_title(
                package_name=kwargs.get('package_name'),
                title=kwargs.get('title')
            )
            package = Package.objects.get(**_kw)
        except Package.DoesNotExist:
            _kw = cls._dict_package_name_or_title(
                package_name=kwargs.get('package_name', default_name_or_title),
                title=kwargs.get('title', default_name_or_title)
            )
            package = Package.objects.create(
                author=cls.create_author_without_ui(context),
                status=kwargs.get('status', 'published'),
                released_datetime=released_datetime,
                **_kw
            )

        if kwargs.get("categories"):
            to_package_categories(package, kwargs.get('categories'))

        if kwargs.get('tags'):
            to_package_tags(package, kwargs.get('tags'))

        package.save()

        if with_version:
            kwargs.update(released_datetime=released_datetime)
            cls.create_package_versions_without_ui(
                context,
                package,
                **kwargs
            )

        if not context.world.get('packages'):
            context.world['packages'] = dict()

        add_model_objects(package)
        context.world.get('packages').update(dict(
            package_name=package.package_name
        ))

        add_model_objects(package)

        return package

    @classmethod
    def _dict_package_name_or_title(cls, package_name, title):
        kw = dict()
        if package_name: kw['package_name'] = package_name
        if title: kw['title'] = title
        return kw

    @classmethod
    @override_settings(PACKAGE_FILE_PARSE_OPTS=dict(
        package_version_parser_class=None,
        package_version_parse_handle_class=None
    ))
    def create_package_versions_without_ui(cls, context, package, **kwargs):
        yesterday = now() - timedelta(days=1)
        released_datetime = kwargs.get('released_datetime', yesterday)
        package |should_not| be(None)
        package_version = PackageVersion.objects.create(
            package=package,
            version_code=kwargs.get('version_code'),
            version_name=kwargs.get('version_name'),
            status=kwargs.get('status', 'published'),
            released_datetime=released_datetime,
            icon=SubFile.icon(),
            cover=SubFile.cover(),
            download=SubFile.package()
        )
        add_model_objects(package_version)

    @classmethod
    def visit_package_detail(cls, context, package):
        from urllib.parse import urljoin
        url = cls.get_package_detail_url(context, package)
        full_url = urljoin(context.base_url, url)
        print('visit_package_detail')
        print(full_url)
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

    @classmethod
    def get_package_by(cls, title=None, package_name=None):
        kw = cls._dict_package_name_or_title(package_name=package_name,
                                             title=title)
        package = Package.objects.get(**kw)
        package.status |should| equal_to(Package.STATUS.published)
        return package

    @classmethod
    def get_packageversion_by(cls, version_code, title=None, package_name=None):
        package = cls.get_package_by(title, package_name)
        packageversion = package.versions.get(version_code=version_code)
        packageversion.status |should| equal_to(PackageVersion.STATUS.published)
        return packageversion

    @classmethod
    def get_package_or_version_by(cls, title=None, package_name=None, version_code=None):
        any((title, package_name, version_code)) |should_not| be(False)

        if version_code is not None:
            return cls.get_packageversion_by(title=title,
                                             package_name=package_name,
                                             version_code=version_code)

        return cls.get_package_by(title=title, package_name=package_name)


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

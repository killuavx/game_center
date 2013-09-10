# -*- encoding=utf-8 -*-
from warehouse.models import Package, Author, PackageVersion, PackageVersionScreenshot
from taxonomy.models import Category
from django.utils.timezone import now, timedelta
import random
import logging

_models = []

def unique_datetime_id():
    id = "%s-%d" %(now().strftime('%Y%m%d%H%M%s'), random.randint(100, 1000))
    return id


def create_category(**defaults):
    logging.info('create_category', defaults)
    defaults.setdefault('name', "Game")
    inst = Category.objects.create(**defaults)
    _models.append(inst)
    return inst

def create_author(**defaults):
    logging.info('create_author', defaults)
    defaults.setdefault('email', 'kent-back@testcase.com')
    defaults.setdefault('name', "Kent Back")
    inst, flag = Author.objects.get_or_create(**defaults)
    _models.append(inst)
    return inst

def create_package(**defaults):
    logging.info('create_package', defaults)
    id = unique_datetime_id()
    defaults.setdefault('title', "fts-dsl game %s" % id)
    defaults.setdefault('package_name', "com.fts.dsl-helper.%s" % id)
    if not defaults.get('author'):
        rdnum = random.randint(1, 1000),
        defaults.setdefault('author', create_author(
            name="tc %d" % rdnum,
            email="tc%d@testcase.com" % rdnum
        ))
    inst = Package.objects.create(**defaults)
    _models.append(inst)
    return inst

def clear_data():
    for m in _models:
        try:  m.delete()
        except: pass

import io
from os.path import join, dirname, abspath
from django.core.files import File
class ApiDSL(object):

    def setUp(self, client, world):
        self.world = world
        self.client = client

    _count = 0

    _fixtures_dir = join(dirname(abspath(__file__)), 'fixtures')

    def Given_i_have_package_with(self, **defaults):
        defaults.setdefault('status', Package.STATUS.published)
        defaults.setdefault('released_datetime', now()-timedelta(days=1))
        return create_package(**defaults)

    def Given_i_have_some_packages(self, num=3, **defaults):
        defaults.setdefault('status', Package.STATUS.published)
        packages = []
        for i in range(num):
            defaults['released_datetime'] =  now()-timedelta(days=i, hours=1)
            packages.append(create_package(**defaults))

        return packages

    def Given_package_version_add_screenshot(self, version):
        pss = PackageVersionScreenshot()
        pss.image = File(io.FileIO(join(ApiDSL._fixtures_dir,'screenshot2.jpg')))
        version.screenshots.add(pss)
        _models.append(pss)
        return pss

    def Then_i_should_see_package_detail_information(self, pkg_detail_data):

        def Then_i_should_see_screenshots_in_package_version( version ):
            fields = (
                'large',
                'preview',
                'rotate',
            )
            for s in version.get('screenshots'):
                for field in fields:
                    self.assertIn(field, s)

        def Then_i_should_see_versions_in_package_detail(package_detail_data):
            fields = (
                'icon',
                'download',
                'version_code',
                'version_name',
                'whatsnew',
            )
            for v in package_detail_data.get('versions'):
                Then_i_should_see_screenshots_in_package_version(v)
                for field in fields:
                    self.assertIn(field, v)

        fields = (
            'url',
            'package_name',
            'title',
            'author',
            'summary',
            'description',
            'screenshots',
            'released_datetime',
            'versions',

        )
        for field in fields:
            self.assertIn(field, pkg_detail_data)

        Then_i_should_see_versions_in_package_detail(pkg_detail_data)

    def When_i_access_packages_newest(self):
        self.world.setdefault('response',
                              self.client.get('/api/newest/packages/'))

    def Then_i_should_receive_success_response(self):
        response = self.world.get('response')
        self.assertEqual(response.status_code, 200)
        content = self.convert_content(response.content)
        self.world.update(dict(response=response, content=content))

    def Then_i_should_see_packages_list(self, num):
        content = self.world.get('content')
        self.assertResultList(content=content,
                              previous=None,
                              next=None,
                              count=num,
                              result_len=num )

    def Then_i_should_see_package_list_order_by_released_datetime_desc(self):
        content = self.world.get('content')
        result = content.get('results')
        self.assertGreater(result[0].get('released_datetime'),
                           result[1].get('released_datetime'))
        self.assertGreater(result[1].get('released_datetime'),
                           result[2].get('released_datetime'))

    def Then_i_should_see_package_summary_information_for_list(self, pkg_data):

        fields = (
            'url',
            'icon',
            'package_name',
            'title',
            'released_datetime',
            'summary',
            'author',
        )
        for field in fields:
            self.assertIn(field, pkg_data)

            #self.assertIsUrl(pkg_data.get('url'))
            #self.assertIsUrl(pkg_data.get('icon'))

    def When_i_access_package_detail(self, package):
        from warehouse.serializers import PackageSummarySerializer
        serializer = PackageSummarySerializer(package)
        repsonse = self.client.get(serializer.data.get('url'))
        self.world.update(dict(response=repsonse))

    def Given_package_has_version_with(self, package,
                                       version_code, version_name, status,
                                       all_datetime, **default):
        version = PackageVersion(
            version_name = version_name,
            version_code = version_code,
            status=status,
            released_datetime=all_datetime,
            updated_datetime=all_datetime,
            created_datetime=all_datetime,
            **default
        )
        version.icon = File(io.FileIO(join(ApiDSL._fixtures_dir,'icon.png')))
        _models.append(version.icon)
        package.versions.add(version)
        return version


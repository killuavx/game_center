# -*- encoding=utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.core.files import File
from fts.tests import helpers
from warehouse.models import PackageScreenshot, Package
from datetime import timedelta
from django.utils.timezone import now
import json
from django import forms
import io
from os.path import join, dirname, abspath

class RestApiTest(TestCase):

    def setUp(self):
        self.world = dict()
        self.client = Client(HTTP_ACCEPT='application/json')

    def convert_content(self, content):
        return json.loads(content.decode('utf-8'))

    def assertResultList(self, content, previous, next, count, result_len):
        self.assertEqual(content['previous'], next)
        self.assertEqual(content['next'], next)
        self.assertEqual(content['count'], count)
        self.assertEqual(len(content['results']), result_len)

    def assertIsUrl(self, url):
        try:
            forms.URLField(required=True).run_validators(url)
        except forms.ValidationError as err:
            self.fail(err.messages)

class ApiDSL(object):
    _count = 0

    _fixtures_dir = join(dirname(abspath(__file__)), 'fixtures')

    # BDD Steps

    def Given_package_add_some_screenshot(self, pkg):
        pss = PackageScreenshot()
        pss.image = File(io.FileIO(join(ApiDSL._fixtures_dir,'screenshot2.jpg')))
        pkg.screenshots.add(pss)

    def Then_i_should_see_package_detail_information(self, pkg_detail_data):
        fields = (
            'url',
            'icon',
            'package_name',
            'title',
            'author',
            'summary',
            'description',
            'screenshots',
            'released_datetime',

        )
        for field in fields:
            self.assertIn(field, pkg_detail_data)

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

        # end BDD Steps

class NewestPackageTest(RestApiTest):

    def tearDown(self):
        helpers.clear_data()
        super(NewestPackageTest, self).tearDown()

    def test_should_see_package_list_all_be_published(self):

        self._count = 0

        def Given_i_have_package_with(num=3, status=None, released_datetime=None):
            self._count+=1
            pkg = helpers.create_package(package_name='com.gamecenter.%d' % self._count,
                                 title='游戏%d' % self._count,
                                 status=status,
                                 released_datetime=released_datetime
            )
            pkg.save()

        # tomorrow will be published
        tomorrow = now()+timedelta(days=1)
        Given_i_have_package_with(num=1,
                                   status=Package.STATUS.published,
                                   released_datetime=tomorrow
                                   )
        # yestoday published
        yestoday = now()-timedelta(days=1)
        Given_i_have_package_with(num=1,
                                   status=Package.STATUS.published,
                                   released_datetime=yestoday
                                   )
        # yestoday unpublished or else status
        Given_i_have_package_with(num=1,
                                   status=Package.STATUS.unpublished,
                                   released_datetime=yestoday
                                   )
        Given_i_have_package_with(num=1,
                                   released_datetime=yestoday,
                                   status=Package.STATUS.draft
                                   )
        ApiDSL.When_i_access_packages_newest(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_packages_list(self,num=1)
        helpers.clear_data()

    def test_should_see_package_list_orderby_released_datetime_desc(self):

        def Given_i_have_some_packages(num=3):
            for i in range(num):
                pkg = helpers.create_package(package_name='com.gamecenter.%d' % i,
                               title='游戏%d' % i,
                               released_datetime=now()-timedelta(days=i,hours=1)
                )
                pkg.status = pkg.STATUS.published
                pkg.save()

        Given_i_have_some_packages(num=3)
        ApiDSL.When_i_access_packages_newest(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_packages_list(self, num=3)
        ApiDSL.Then_i_should_see_package_list_order_by_released_datetime_desc(self)

    def test_should_see_package_summary_information_for_list(self):

        helpers.create_package(package_name='com.gamecenter.rpg1',
                                     title='rpg 游戏 A',
                                     status=Package.STATUS.published,
                                     released_datetime=now()-timedelta(days=1)
        )
        ApiDSL.When_i_access_packages_newest(self)
        ApiDSL.Then_i_should_receive_success_response(self)

        ApiDSL.Then_i_should_see_packages_list(self,num=1)
        pkg_data = self.world.get('content').get('results')[0]
        ApiDSL.Then_i_should_see_package_summary_information_for_list(self,pkg_data)
        helpers.clear_data()

    def test_should_see_package_detail_information_in_detail(self):

        pkg = helpers.create_package(package_name='com.gamecenter.rpg1',
                               title='rpg 游戏 A',
                               status=Package.STATUS.published,
                               released_datetime=now()-timedelta(days=1)
        )
        ApiDSL.Given_package_add_some_screenshot(self, pkg)
        ApiDSL.When_i_access_package_detail(self, pkg)

        ApiDSL.Then_i_should_receive_success_response(self,)
        ApiDSL.Then_i_should_see_package_detail_information(self,
            pkg_detail_data=self.world.get('content')
        )
        helpers.clear_data()

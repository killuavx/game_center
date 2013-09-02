# -*- encoding=utf-8 -*-
from django.test.testcases import TestCase
from django.test.client import Client
from warehouse.tests.helpers import *
import json


class ApiTest(TestCase):

    def setUp(self):
        self.client = Client(HTTP_ACCEPT='application/json')

    def convert_content(self, content):
        return json.loads(content.decode('utf-8'))

    def assertResultList(self, content, previous, next, count, result_len):
        self.assertEqual(content['previous'], next)
        self.assertEqual(content['next'], next)
        self.assertEqual(content['count'], count)
        self.assertEqual(len(content['results']), result_len)


class ApiRootTest(ApiTest):

    def test_api_root(self):
        response = self.client.get('/api/')
        self.assertEqual(200, response.status_code)

        content = self.convert_content(response.content)
        self.assertIn('packages', content)
        self.assertIn('authors', content)
        self.assertIn('categories', content)

from warehouse.models import Package
from warehouse.serializers import PackageSummarySerializer
class ApiPackageTest(ApiTest):

    def _request_api_status_200(self):
        response = self.client.get('/api/packages/')
        self.assertEqual(200, response.status_code)
        return response

    def test_list(self):
        package = create_package(package_name="com.xianjian",
                                 title='大富翁',
                                 tags='hot new top',
                                 summary="大富翁 3",
                                 status=Package.STATUS.published)
        response = self._request_api_status_200()
        content = self.convert_content(response.content)

        serializer = PackageSummarySerializer(package)
        sd = serializer.data
        self.assertResultList(content,
                              previous=None,
                              next=None,
                              count=1,
                              result_len=1)
        except_pkg = content['results'][0]
        self.assertEqual(except_pkg['package_name'], sd.get('package_name'))
        self.assertEqual(except_pkg['author']['name'], sd.get('author').get('name'))
        self.assertEqual(except_pkg['title'], sd.get('title'))
        self.assertEqual(except_pkg['released_datetime'], sd.get('released_datetime'))
        self.assertEqual(except_pkg['tags'], sd.get('tags'))


from warehouse.models import Author
from warehouse.serializers import AuthorSerializer, AuthorSummarySerializer
class ApiAuthorTest(ApiTest):

    def _request_api_status_200(self):
        response = self.client.get('/api/authors/')
        self.assertEqual(200, response.status_code)
        return response

    def test_list(self):
        author = create_author(name="Robert C. Martin",
                                email='uncle-rob@dev.com',
                                phone='86-021-82901929',
                                status=Author.STATUS.activated)
        response = self._request_api_status_200()
        content = self.convert_content(response.content)

        serializer = AuthorSummarySerializer(author)
        sd = serializer.data
        self.assertResultList(content,
                              previous=None,
                              next=None,
                              count=1,
                              result_len=1)
        except_author = content['results'][0]
        self.assertEqual(except_author['name'], sd.get('name'))
        self.assertNotIn('email', except_author)
        self.assertNotIn('phone', except_author)


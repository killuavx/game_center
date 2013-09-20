# -*- encoding=utf-8 -*-
from django.test.client import Client
from django.test.testcases import TestCase
import json
from taxonomy.tests.helpers import *
from mobapi.serializers import CategorySummarySerializer, CategoryDetailSerializer

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

class ApiCategoryTest(ApiTest):

    def _request_api_status_200(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(200, response.status_code)
        return response

    def _request_detail_status_200(self, category):
        response = self.client.get('/api/categories/%s/' % category.slug)
        self.assertEqual(200, response.status_code)
        return response

    def test_list_category(self):
        category = create_category()
        response = self._request_api_status_200()
        content = self.convert_content(response.content)
        self.assertResultList(content,
                              previous=None,
                              next=None,
                              count=1,
                              result_len=1)
        serializer = CategorySummarySerializer(category)
        sd = serializer.data
        except_cat = content.get('results')[0]
        self.assertIn('icon', except_cat)
        self.assertIn('url', except_cat)
        self.assertEqual(sd.get('name'), except_cat.get('name'))
        self.assertEqual(sd.get('slug'), except_cat.get('slug'))

    def test_detail_category(self):
        category = create_category(name="RPG")
        response = self._request_detail_status_200(category)
        content = self.convert_content(response.content)

        serializer = CategoryDetailSerializer(category)
        sd = serializer.data
        except_cat = content
        self.assertIn('url', except_cat)
        self.assertIn('icon', except_cat)
        self.assertEqual(sd.get('name'), except_cat.get('name'))
        self.assertEqual(sd.get('slug'), except_cat.get('slug'))
        self.assertIn('packages_url', except_cat)


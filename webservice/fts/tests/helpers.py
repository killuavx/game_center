# -*- encoding=utf-8 -*-
import io
import os
from os.path import join, dirname, abspath
from django.test.testcases import TestCase
from django.test.client import Client
from django import forms
import json
from django.core.files import File
from searcher.models import TipsWord
from warehouse.models import Package, Author, PackageVersion, PackageVersionScreenshot
from taxonomy.models import Category, Topic, TopicalItem
from account.models import Player
from rest_framework.authtoken.models import Token
from django.utils.timezone import now, timedelta
from urllib import parse as urlparse

import random
_models = []
_files = []


def guid():
    def S4():
        return hex(int(((1 + random.random()) * 0x10000) or 0))[2:]
    return "%s-%s-%s-%s"%(S4(), S4(), S4(), S4())

def create_category(**defaults):
    defaults.setdefault('name', "Game")
    inst = Category.objects.create(**defaults)
    _models.append(inst)
    return inst

def create_author(**defaults):
    defaults.setdefault('email', 'kent-back@testcase.com')
    defaults.setdefault('name', "Kent Back")
    inst, flag = Author.objects.get_or_create(**defaults)
    _models.append(inst)
    return inst

def create_package(**defaults):
    id = guid()
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

def create_topic(**defaults):
    id = guid()
    defaults.setdefault('name', 'topic %s' %id)
    defaults.setdefault('slug', 'topic-%s' %id)
    inst = Topic.objects.create(**defaults)
    _models.append(inst)
    return inst

def create_topicalitem(topic, item):
    inst = TopicalItem.objects.create(topic=topic, content_object=item)
    _models.append(inst)
    return inst

def create_tipsword(**defaults):
    inst = TipsWord.objects.create(**defaults)
    _models.append(inst)
    return inst

def create_account(**default):
    gid = guid()
    default.setdefault('username', "player-%s"%gid)
    default.setdefault('email', '%s@testcase.com'%gid)

    def rint():
        return str(random.randint(10,99))

    default.setdefault('phone', '+86-021-%s%s%s%s'%(rint(), rint(), rint(), rint()))
    inst = Player.objects.create_user(**default)
    _models.append(inst)
    return inst

def create_auth_token(user):
    token, is_newed = Token.objects.get_or_create(user=user)
    _models.append(token)
    return token.key

def clear_data():
    for m in _models:
        try:  m.delete()
        except: pass

    for f in _files:
        try:
            os.remove(f)
        except:pass

class ApiDSL():

    def setUp(self, client, world):
        self.world = world
        self.client = client

    _count = 0

    _fixtures_dir = join(dirname(abspath(__file__)), 'fixtures')

    def Given_i_have_package_with(self, **defaults):
        defaults.setdefault('released_datetime', now()-timedelta(days=1))
        return create_package(**defaults)

    def Given_i_have_some_packages(self, num=3, **defaults):
        defaults.setdefault('status', Package.STATUS.published)
        packages = []
        for i in range(num):
            defaults['released_datetime'] =  now()-timedelta(days=i, hours=1)
            packages.append(create_package(**defaults))

        return packages

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
        _files.append(version.icon.path)
        return version

    def Given_package_version_add_screenshot(self, version):
        pss = PackageVersionScreenshot()
        pss.image = File(io.FileIO(join(ApiDSL._fixtures_dir,'screenshot2.jpg')))
        version.screenshots.add(pss)
        _models.append(pss)
        return pss

    def Given_i_have_cover_image(self):
        return File(io.FileIO(join(ApiDSL._fixtures_dir,'icon.png')))

    def Given_i_have_icon_image(self):
        return File(io.FileIO(join(ApiDSL._fixtures_dir,'icon.png')))

    def Given_i_have_activated_author(self, **kwargs):
        kwargs.setdefault('status', Author.STATUS.activated)
        return create_author(**kwargs)

    def Given_i_have_published_package(self, all_datetime=now()-timedelta(days=1), **kwargs):
        pkg = ApiDSL.Given_i_have_package_with(self,
                                               status=Package.STATUS.published,
                                               **kwargs)
        version = ApiDSL.Given_package_has_version_with(self,
                                                        pkg,
                                                        version_code=1,
                                                        version_name='1.0beta',
                                                        status=PackageVersion.STATUS.published,
                                                        all_datetime=all_datetime)
        ApiDSL.Given_package_version_add_screenshot(self, version)
        return pkg

    def Given_i_have_topic_with(self, all_datetime, **defaults):
        defaults.setdefault('created_datetime', all_datetime)
        defaults.setdefault('updated_datetime', all_datetime)
        defaults.setdefault('released_datetime', all_datetime)
        return create_topic(**defaults)

    def Given_topic_add_item(self, topic, item):
        return create_topicalitem(topic, item)

    def Given_i_have_tipsword_with(self, **default):
        return create_tipsword(**default)

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
                'cover',
                'download',
                'download_count',
                'download_size',
                'screenshots',
                'version_code',
                'version_name',
                'whatsnew',
            )
            for v in package_detail_data.get('versions'):
                Then_i_should_see_screenshots_in_package_version(v)
                for field in fields:
                    self.assertIn(field, v)

        def Then_i_should_see_actions_in_package_detail(package_detail_data):
            fields = (
                'mark',
            )
            actions = package_detail_data.get('actions')
            for f in fields:
                self.assertIn(f, actions)

        fields = (
            'url',
            'icon',
            'cover',
            'version_code',
            'version_name',
            'download',
            'download_count',
            'download_size',
            'whatsnew',
            'package_name',
            'title',
            'author',
            'summary',
            'description',
            'screenshots',
            'released_datetime',
            'versions',
            'category_name',
            'categories_names',
            'actions',
        )
        for field in fields:
            self.assertIn(field, pkg_detail_data)

        Then_i_should_see_actions_in_package_detail(pkg_detail_data)
        Then_i_should_see_versions_in_package_detail(pkg_detail_data)

    def Then_i_should_see_package_detail_contains_categories_names(self, pkg_data, cat_names):
        self.assertListEqual(pkg_data.get('categories_names'), list(cat_names))

    def When_i_access_api_root(self):
        response = self.client.get('/api/')
        self.world.setdefault('response', response)

    def Then_i_should_see_the_api_in_content(self, name):
        self.assertIn(name, self.world.get('content'))

    def When_i_access_category_list(self):
        res = self.client.get('/api/categories/')
        self.world.setdefault('response', res)

    def When_i_access_category_detail(self, category):
        res = self.client.get('/api/categories/%s/'%category.slug)
        self.world.setdefault('response', res)

    def When_i_access_topic_list(self, topic=None):
        if topic:
            res = self.client.get('/api/topics/%s/children/' % topic.slug)
        else:
            res = self.client.get('/api/topics/')
        self.world.setdefault('response', res)

    def When_i_access_topic_detail(self, topic):
        res = self.client.get('/api/topics/%s/' % topic.slug)
        self.world.setdefault('response', res)

    def When_i_access_topic_items(self, topic):
        respose = self.client.get('/api/topics/%s/items/' % topic.slug)
        self.world.setdefault('response', respose)

    def When_i_access_author_packages(self, author):
        respose = self.client.get('/api/authors/%s/packages/' % author.pk)
        self.world.setdefault('response', respose)

    def When_i_access_topic_newest_package(self):
        # note: path没有以"/"结束
        response = self.client\
            .get('/api/topics/newest/items?ordering=-released_datetime',
                 follow=True)
        self.world.setdefault('response',  response)

    def When_i_access_search_package(self, keyword):
        response = self.client \
            .get('/api/search?q=%s' % urlparse.quote_plus(keyword),
                 follow=True)
        self.world.setdefault('response',  response)

    def When_i_access_search_tips(self):
        response = self.client \
            .get('/api/tipswords', follow=True)
        self.world.setdefault('response',  response)

    def When_i_access_rankings_list(self, rankings_type):
        res = self.client.get('/api/rankings/')
        self.world.setdefault('response', res)

    def When_i_access_advertisement_with(self, place=None):
        if place:
            res = self.client.get('/api/advertisements/?place=%s'%place.slug)
        else:
            res = self.client.get('/api/advertisements/')

        self.world.setdefault('response', res)


    def Then_i_should_see_tips_list(self, tips_list):
        for t in tips_list:
            return ApiDSL.Then_i_should_see_tips(self, t)

    def Then_i_should_see_tips(self, tips):
        self.assertIn('keyword', tips)
        self.assertIn('weight', tips)

    def Then_i_should_receive_success_response(self):
        response = self.world.get('response')
        self.assertEqual(response.status_code, 200)
        content = self.convert_content(response.content)
        self.world.update(dict(response=response, content=content))

    def Then_i_should_receive_response_with(self, status_code=None):
        response = self.world.get('response')
        self.assertEqual(response.status_code, status_code)
        content = self.convert_content(response.content)
        self.world.update(dict(response=response, content=content))
        self.world.update(dict(response=response, content=content))

    def Then_i_should_see_result_list(self, num, count=None, previous=None, next=None):
        content = self.world.get('content')
        count = num if count is None else count
        self.assertResultList(content=content,
                              previous=previous,
                              next=next,
                              count=count,
                              result_len=num )

    def Then_i_should_see_package_list_order_by_download_count_desc(self):
        content = self.world.get('content')
        result = content.get('results')
        self.assertGreater(result[0].get('download_count'),
                           result[1].get('download_count'))

    def Then_i_should_see_package_list_order_by_released_datetime_desc(self):
        content = self.world.get('content')
        result = content.get('results')
        self.assertGreater(result[0].get('released_datetime'),
                           result[1].get('released_datetime'))
        self.assertGreater(result[1].get('released_datetime'),
                           result[2].get('released_datetime'))

    def Then_i_should_see_package_summary_list(self, pkg_list_data):
        for p in pkg_list_data:
            ApiDSL\
                .Then_i_should_see_package_summary_information_for_list(self, p)

    def Then_i_should_see_package_summary_information_for_list(self, pkg_data):
        fields = (
            'url',
            'icon',
            'cover',
            'package_name',
            'title',
            'category_name',
            'categories_names',
            'tags',
            'version_count',
            'released_datetime',
            'summary',
            'author',
            'actions',
        )
        for field in fields:
            self.assertIn(field, pkg_data)

        actions = (
            'mark',
        )
        for field in actions:
            self.assertIn(field, pkg_data.get('actions'))

    def Then_i_should_see_author_summary_list(self, author_list_data):
        for a in author_list_data:
            ApiDSL.Then_i_should_see_author_summary_info(self, a)

    def Then_i_should_see_author_summary_info(self, author_data):
        fields = (
            'url',
            'icon',
            'cover',
            'name',
            'packages_url',
        )
        for field in fields:
            self.assertIn(field, author_data)

    def Then_i_should_see_topic_list(self, topic_list_data):
        for t in topic_list_data:
            ApiDSL.Then_i_should_see_topic_summary_info(self, t)

    def Then_i_should_see_topic_summary_info(self, topic_data):
        fields = (
            'url',
            'icon',
            'cover',
            'name',
            'slug',
            'children_url',
            'items_url',
            'items_count',
            'updated_datetime',
            'released_datetime',
        )
        for field in fields:
            self.assertIn(field, topic_data)

    def Then_i_should_see_topic_detail(self, topic_data):
        fields = (
            'url',
            'icon',
            'cover',
            'name',
            'slug',
            'summary',
            'children_url',
            'items_url',
            'items_count',
            'updated_datetime',
            'released_datetime',
        )
        for field in fields:
            self.assertIn(field, topic_data)

    def Then_i_should_see_category_detail(self, cat_data):
        fields = (
            'url',
            'icon',
            'name',
            'slug',
            'packages_url',
        )
        for field in fields:
            self.assertIn(field, cat_data)

    def When_i_access_package_detail(self, package):
        from mobapi.serializers import PackageSummarySerializer
        serializer = PackageSummarySerializer(package)
        repsonse = self.client.get(serializer.data.get('url'))
        self.world.update(dict(response=repsonse))

    def Then_i_should_see_advertisement_list(self, adv_list):

        def Then_i_should_see_advertisement_summary(adv):
            fields = (
                'title',
                'cover',
                'content_type',
                'content_url',
            )
            for f in fields:
                self.assertIn(f, adv)

        for a in adv_list:
            Then_i_should_see_advertisement_summary(a)

    def When_i_signup_with(self, user_data):
        response = self.client.post('/api/accounts/signup/', user_data)
        self.world.update(dict(response=response))

    def When_i_signup_with_querystr(self, query):
        response = self.client.post('/api/accounts/signup/', HTTP_CONTENT=query)
        self.world.update(dict(response=response))

    def When_i_signin_with(self, signin_data):
        response = self.client.post('/api/accounts/signin/', signin_data)
        self.world.update(dict(response=response))

    def Given_i_have_account(self, signin_data=dict()):
        user = create_account(**signin_data)
        return user

    def Given_i_have_signup(self, user):
        token_key = create_auth_token(user)
        headers = dict(HTTP_AUTHORIZATION='Token %s'%token_key)
        self.world.update(dict(headers=headers))

    def When_i_signout(self):
        headers = self.world.get('headers', dict())
        res = self.client.get('/api/accounts/signout/', **headers)
        self.world.update(dict(response=res))

    def Then_i_should_receive_auth_token(self):
        content = self.world.get('content')
        self.assertEqual(len(content.get('token')), 40)

    def When_i_prepare_auth_token(self, token):
        headers = dict(HTTP_AUTHORIZATION='Token %s'%token)
        self.world.update(dict(headers=headers))

    def When_i_access_myprofile(self):
        headers = self.world.get('headers', dict())
        res = self.client.get('/api/accounts/myprofile', **headers)
        self.world.update(dict(response=res))

    def Then_i_should_see_myprofile_information(self, user_profile):
        content = self.world.get('content')
        self.assertEqual(content.get('username'), user_profile.get('username'))
        self.assertEqual(content.get('email'), user_profile.get('email'))
        self.assertEqual(content.get('phone'), user_profile.get('phone'))
        self.assertIn('icon', content)

    def When_i_access_mybookmarks(self):
        headers = self.world.get('headers', dict())
        res = self.client.get('/api/bookmarks/', **headers)
        self.world.update(dict(response=res))

    def When_i_add_bookmark(self, pkg):
        headers = self.world.get('headers', dict())
        postdata = dict(package_name=pkg.package_name)
        res = self.client.post('/api/bookmarks/', postdata, **headers)
        self.world.update(dict(response=res))

    def When_i_remove_bookmark(self, pkg):
        headers = self.world.get('headers', dict())
        res = self.client.delete('/api/bookmarks/%d/' % pkg.pk, **headers)
        self.world.update(dict(response=res))

    def When_i_access_bookmark_check(self, pkg):
        headers = self.world.get('headers', dict())
        res = self.client.head('/api/bookmarks/%d/' % pkg.pk, **headers)
        self.world.update(dict(response=res))

    def When_i_access_bookmark_check_with(self, **kwargs):
        query = urlparse.urlencode(kwargs)
        headers = self.world.get('headers', dict())
        res = self.client.head('/api/bookmarks/?%s'%query, **headers)
        self.world.update(dict(response=res))

    def When_i_access_url_with_head_method(self, url):
        headers = self.world.get('headers', dict())
        res = self.client.head(url, **headers)
        self.world.update(dict(response=res))

    def clear_world(self):
        self.world = {}

class RestApiTest(TestCase):

    def setUp(self):
        self.world = dict()
        self.client = Client(HTTP_ACCEPT='application/json',
                             HTTP_CACHE_CONTROL='no-cache')
        ApiDSL.setUp(self, client=self.client, world=self.world)

    def convert_content(self, content):
        try:
            return json.loads(content.decode('utf-8'))
        except:
            return content.decode('utf-8')

    def assertResultList(self, content, previous, next, count, result_len):
        self.assertIsInstance(content.get('results'), list)
        self.assertEqual(content['count'], count)
        self.assertEqual(len(content['results']), result_len)
        self.assertEqual(content['previous'], previous)
        self.assertEqual(content['next'], next)

    def assertIsUrl(self, url):
        try:
            forms.URLField(required=True).run_validators(url)
        except forms.ValidationError as err:
            self.fail(err.messages)

    def tearDown(self):
        clear_data()
        super(RestApiTest, self).tearDown()


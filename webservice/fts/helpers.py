# -*- encoding=utf-8 -*-
import io
import os
from os.path import join, dirname, abspath
import json
from urllib import parse as urlparse
from collections import namedtuple

from django.test.testcases import TestCase
from django.test.client import Client
from django import forms
from django.core.files import File
from django.db.models.signals import pre_save
from rest_framework.authtoken.models import Token
from django.utils.timezone import now, timedelta
from should_dsl import should

from searcher.models import TipsWord
from warehouse.models import Package, Author, PackageVersion, PackageVersionScreenshot
from warehouse.models import package_version_pre_save
from taxonomy.models import Category, Topic, TopicalItem
from account.models import User as Player
from toolkit.middleware import get_current_request
from mobapi.warehouse.serializers.package import PackageSummarySerializer, PackageDetailSerializer


fixtures_dir = join(dirname(abspath(__file__)), 'fixtures')

StatusCode = namedtuple('StatusCode', ['code', 'reason'])

import random

_models = []
_files = []


def guid():
    def S4():
        return hex(int(((1 + random.random()) * 0x10000) or 0))[2:]

    return "%s-%s-%s-%s" % (S4(), S4(), S4(), S4())


def add_model_objects(*args):
    _models.extend(args)


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


def create_packageversion(package, **default):
    inst = PackageVersion.objects.create(package=package,
                                         **default)
    _models.append(inst)
    return inst


def create_packageversionscreenshot(**defaults):
    id = guid()
    defaults.setdefault('alt', 'alt-%s' % id)
    inst = PackageVersionScreenshot(**defaults)
    _models.append(inst)
    return inst


def create_topic(**defaults):
    id = guid()
    defaults.setdefault('name', 'topic %s' % id)
    defaults.setdefault('slug', 'topic-%s' % id)
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
    default.setdefault('username', "player-%s" % gid)
    default.setdefault('email', '%s@testcase.com' % gid)

    def rint():
        return str(random.randint(10, 99))

    default.setdefault('phone',
                       '+86-021-%s%s%s%s' % (rint(), rint(), rint(), rint()))
    inst = Player.objects.create_user(**default)
    _models.append(inst)
    return inst


def create_auth_token(user):
    token, is_newed = Token.objects.get_or_create(user=user)
    _models.append(token)
    return token.key


def clear_data():
    while True:
        try:
            m = _models.pop()
            m.delete()
        except AssertionError:
            pass
        except IndexError:
            break

    while True:
        f = None
        try:
            f = _files.pop()
        except IndexError:
            break
        try:
            os.remove(f)
        except:
            pass


def convert_content(content):
    try:
        content = content.decode('utf-8')
    except:
        pass

    try:
        return json.loads(content)
    except:
        return content


def disconnect_packageversion_pre_save():
    pre_save.disconnect(package_version_pre_save, PackageVersion)


def connect_packageversion_pre_save():
    pre_save.connect(package_version_pre_save, PackageVersion)


def _world_response_status(context, res):
    context.world.update(dict(
        response=res,
        content=convert_content(res.content),
        status=StatusCode(
            code=res.status_code,
            reason=res.status_text
        )
    ))


def sub_file_package():
    return join(fixtures_dir, 'tinysize.apk')


class SubFile(object):

    fixtures_dir = fixtures_dir

    @classmethod
    def package(cls):
        name = 'tinysize.apk'
        return cls.file(name)

    @classmethod
    def icon(cls):
        name = 'icon.png'
        return cls.file(name)

    @classmethod
    def cover(cls):
        name = 'cover.jpg'
        return cls.file(name)

    @classmethod
    def screenshot(cls):
        name = 'screenshot1.jpg'
        return cls.file(name)


    @classmethod
    def file(cls, name):
        return File(io.FileIO(join(cls.fixtures_dir, name)))

    @classmethod
    def fixture_filename(cls, name):
        return join(fixtures_dir, name)


class RestApiTest(TestCase):
    def setUp(self):
        self.world = dict()
        self.client_initial_params = dict(HTTP_ACCEPT='application/json',
                                          HTTP_CACHE_CONTROL='no-cache')
        self.client = Client(**self.client_initial_params)

    def convert_content(self, content):
        return convert_content(content)

    def assertResultList(self, content, previous, next, count, result_len):
        content.get('results') | should | be_kind_of(list)
        content['count'] | should | equal_to(count)
        len(content['results']) | should | equal_to(result_len)
        content['previous'] | should | equal_to(previous)
        content['next'] | should | equal_to(next)

    def tearDown(self):
        clear_data()
        super(RestApiTest, self).tearDown()


class ApiDSL(RestApiTest):
    def convert_content(self, content):
        return convert_content(content)

    def assertResultList(self, content, previous, next, count, result_len):
        content.get('results') | should | be_kind_of(list)
        content['count'] | should | equal_to(count)
        len(content['results']) | should | equal_to(result_len)
        content['previous'] | should | equal_to(previous)
        content['next'] | should | equal_to(next)

    def assertIsUrl(self, url):
        try:
            forms.URLField(required=True).run_validators(url)
        except forms.ValidationError as err:
            self.fail(err.messages)

    _count = 0

    _fixtures_dir = join(dirname(abspath(__file__)), 'fixtures')

    def Given_i_have_package_with(self, **defaults):
        defaults.setdefault('released_datetime', now() - timedelta(days=1))
        return create_package(**defaults)

    def _Given_i_have_some_packages(self, num=3, **defaults):
        defaults.setdefault('status', Package.STATUS.published)
        packages = []
        for i in range(num):
            defaults['released_datetime'] = now() - timedelta(days=i, hours=1)
            packages.append(create_package(**defaults))

        return packages

    def Given_package_has_version_with(self, package,
                                       version_code, version_name,
                                       status,
                                       all_datetime, **default):
        version = PackageVersion(
            version_name=version_name,
            version_code=version_code,
            status=status,
            released_datetime=all_datetime,
            updated_datetime=all_datetime,
            created_datetime=all_datetime,
            **default
        )
        version.icon = File(io.FileIO(join(ApiDSL._fixtures_dir, 'icon.png')))
        _models.append(version.icon)
        package.versions.add(version)
        _files.append(version.icon.path)
        return version

    def Given_package_version_add_screenshot(self, version):
        pss = PackageVersionScreenshot()
        pss.image = File(
            io.FileIO(join(ApiDSL._fixtures_dir, 'screenshot2.jpg')))
        version.screenshots.add(pss)
        _models.append(pss)
        return pss

    def Given_i_have_cover_image(self):
        return File(io.FileIO(join(ApiDSL._fixtures_dir, 'icon.png')))

    def Given_i_have_icon_image(self):
        return File(io.FileIO(join(ApiDSL._fixtures_dir, 'icon.png')))

    def Given_i_have_activated_author(self, **kwargs):
        kwargs.setdefault('status', Author.STATUS.activated)
        return create_author(**kwargs)

    def Given_i_have_published_package(self,
                                       all_datetime=now() - timedelta(days=1),
                                       **kwargs):
        vkwargs = dict()
        try:
            vkwargs['version_code'] = kwargs.pop('version_code')
        except:
            pass
        try:
            vkwargs['version_name'] = kwargs.pop('version_name')
        except:
            pass

        pkg = ApiDSL.Given_i_have_package_with(self,
                                               status=Package.STATUS.published,
                                               **kwargs)
        version = ApiDSL.Given_package_has_version_with(self,
                                                        pkg,
                                                        version_code=vkwargs.get(
                                                            'version_code', 1),
                                                        version_name=vkwargs.get(
                                                            'version_name',
                                                            '1.0beta'),
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

        def Then_i_should_see_screenshots_in_package_version(version):
            fields = (
                'large',
                'preview',
                'rotate',
            )
            for s in version.get('screenshots'):
                s | should | include_keys(*fields)

        def Then_i_should_see_versions_in_package_detail(package_detail_data):
            fields = (
                'icon',
                'cover',
                'download',
                'download_count',
                'download_size',
                'comment_count',
                'comments_url',
                'screenshots',
                'version_code',
                'version_name',
                'whatsnew',
            )
            for v in package_detail_data.get('versions'):
                Then_i_should_see_screenshots_in_package_version(v)
                v | should | include_keys(*fields)

        def Then_i_should_see_actions_in_package_detail(package_detail_data):
            fields = (
                'mark',
            )
            actions = package_detail_data.get('actions')
            actions | should | include_keys(*fields)

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
            'versions_url',
            'category_name',
            'categories_names',
            'actions',
        )
        pkg_detail_data | should | include_keys(*fields)

        Then_i_should_see_actions_in_package_detail(pkg_detail_data)

    def Then_i_should_see_package_detail_contains_categories_names(self,
                                                                   pkg_data,
                                                                   cat_names):
        pkg_data.get('categories_names') | should | include_in_any_order(
            list(cat_names))

    def When_i_access_api_root(self):
        res = self.client.get('/api/')
        _world_response_status(self, res)

    def Then_i_should_see_the_api_in_content(self, name):
        self.world.get('content') | should | include_keys(name)

    def When_i_access_category_list(self):
        res = self.client.get('/api/categories/')
        _world_response_status(self, res)

    def When_i_access_category_detail(self, category):
        res = self.client.get('/api/categories/%s/' % category.slug)
        _world_response_status(self, res)

    def Then_i_should_see_the_category_in_category_tree(self, category,
                                                        flag=True):
        category_tree = self.world.get('content')

        def _tree_contains_category(tree, category):
            for element in tree:
                if element.get('slug') == category.slug:
                    return True
                else:
                    flag = _tree_contains_category(element.get('children'),
                                                   category)
                    if flag:
                        return True
            return False

        _tree_contains_category(category_tree, category) | should | be(flag)

    def When_i_access_topic_list(self, topic=None):
        if topic:
            res = self.client.get('/api/topics/%s/children/' % topic.slug)
        else:
            res = self.client.get('/api/topics/')
        _world_response_status(self, res)

    def When_i_access_topic_detail(self, topic):
        res = self.client.get('/api/topics/%s/' % topic.slug)
        _world_response_status(self, res)

    def When_i_access_topic_items(self, topic):
        res = self.client.get('/api/topics/%s/items/' % topic.slug)
        _world_response_status(self, res)

    def When_i_access_author_packages(self, author):
        res = self.client.get('/api/authors/%s/packages/' % author.pk)
        _world_response_status(self, res)

    def When_i_access_topic_newest_package(self):
        # note: path没有以"/"结束
        res = self.client \
            .get('/api/topics/newest/items?ordering=-released_datetime',
                 follow=True)
        _world_response_status(self, res)

    def When_i_access_search_package(self, keyword):
        res = self.client \
            .get('/api/search?q=%s' % urlparse.quote_plus(keyword),
                 follow=True)
        _world_response_status(self, res)

    def When_i_access_search_tips(self):
        res = self.client \
            .get('/api/tipswords', follow=True)
        _world_response_status(self, res)

    def When_i_access_rankings_list(self, rankings_type):
        res = self.client.get('/api/rankings/')
        _world_response_status(self, res)

    def When_i_access_advertisement_with(self, place=None):
        if place:
            res = self.client.get('/api/advertisements/?place=%s' % place.slug)
        else:
            res = self.client.get('/api/advertisements/')

        _world_response_status(self, res)

    def Then_i_should_see_tips_list(self, tips_list):
        for t in tips_list:
            return ApiDSL.Then_i_should_see_tips(self, t)

    def Then_i_should_see_tips(self, tips):
        fields = ('keyword', 'weight')
        tips | should | include_keys(*fields)

    def Then_i_should_receive_success_response(self):
        response = self.world.get('response')
        response.status_code | should | equal_to(200)
        content = convert_content(response.content)
        self.world.update(dict(response=response, content=content))

    def Then_i_should_receive_response_with(self, status_code=None):
        response = self.world.get('response')
        content = None
        if response.content:
            content = convert_content(response.content)
        response.status_code | should | equal_to(status_code)
        self.world.update(dict(response=response, content=content))

    def Then_i_should_see_result_list(self, num, count=None, previous=None,
                                      next=None):
        content = self.world.get('content')
        count = num if count is None else count
        self.assertResultList(content=content,
                              previous=previous,
                              next=next,
                              count=count,
                              result_len=num)

    def Then_i_should_see_package_list_order_by_download_count_desc(self):
        content = self.world.get('content')
        result = content.get('results')
        result[0].get('download_count') |should| be_greater_than(
            result[1].get('download_count'))

    def Then_i_should_see_package_list_order_by_released_datetime_desc(self):
        content = self.world.get('content')
        result = content.get('results')
        result[0].get('released_datetime') |should| be_greater_than(
            result[1].get('released_datetime'))
        result[1].get('released_datetime') |should| be_greater_than(
            result[2].get('released_datetime'))

    def Then_i_should_see_package_summary_list(self, pkg_list_data):
        for p in pkg_list_data:
            ApiDSL \
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
            'comments_url',
            'download_size',
            'released_datetime',
            'summary',
            'author',
            'actions',
        )
        pkg_data | should | include_keys(*fields)

        actions = (
            'mark',
        )
        pkg_data.get('actions') | should | include_keys(*actions)

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
        author_data | should | include_keys(*fields)

    def Then_i_should_see_account_profile(self, profile_data):
        fields = (
            'icon',
            'username',
            'phone',
            'email',
        )
        profile_data | should | include_keys(*fields)

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
        topic_data | should | include_keys(*fields)

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
        topic_data | should | include_keys(*fields)

    def Then_i_should_see_category_detail(self, cat_data):
        fields = (
            'url',
            'icon',
            'name',
            'slug',
            'packages_url',
        )
        cat_data | should | include_keys(*fields)

    def When_i_access_package_detail(self, package):

        serializer = PackageSummarySerializer(package, context=dict(
            request=get_current_request()))
        res = self.client.get(serializer.data.get('url'))
        _world_response_status(self, res)

    def Then_i_should_see_advertisement_list(self, adv_list):

        def Then_i_should_see_advertisement_summary(adv):
            fields = (
                'title',
                'cover',
                'content_type',
                'content_url',
            )
            adv | should | include_keys(*fields)

        for a in adv_list:
            Then_i_should_see_advertisement_summary(a)

    def When_i_signup_with(self, user_data):
        res = self.client.post('/api/accounts/signup/', user_data)
        _world_response_status(self, res)

    def When_i_signup_with_querystr(self, query):
        res = self.client.post('/api/accounts/signup/', HTTP_CONTENT=query)
        _world_response_status(self, res)

    def When_i_signin_with(self, signin_data):
        res = self.client.post('/api/accounts/signin/', signin_data)
        _world_response_status(self, res)

    def Given_i_have_account(self, signin_data=dict()):
        user = create_account(**signin_data)
        return user

    def Given_i_have_signup(self, user):
        token_key = create_auth_token(user)
        headers = dict(HTTP_AUTHORIZATION='Token %s' % token_key)
        self.world.update(dict(headers=headers))
        ApiDSL.When_i_prepare_auth_token(self, token_key)

    def When_i_signout(self):
        headers = self.world.get('headers', dict())
        res = self.client.get('/api/accounts/signout/', **headers)
        _world_response_status(self, res)

        try:
            self.client_initial_params.pop('HTTP_AUTHORIZATION')
        except:
            pass
        self.client = Client(**self.client_initial_params)

    def Then_i_should_receive_auth_token(self):
        content = self.world.get('content')
        len(content.get('token')) | should | equal_to(40)

    def When_i_prepare_auth_token(self, token):
        headers = dict(HTTP_AUTHORIZATION='Token %s' % token)
        self.world.update(dict(headers=headers))
        self.client_initial_params.update(headers)
        self.client = Client(**self.client_initial_params)

    def When_i_access_myprofile(self):
        headers = self.world.get('headers', dict())
        res = self.client.get('/api/accounts/myprofile', **headers)
        _world_response_status(self, res)

    def Then_i_should_see_myprofile_information(self, user_profile,
                                                fields=('username', )):
        content = self.world.get('content')
        for field in fields:
            content.get(field) |should| equal_to(user_profile.get(field))

    def When_i_access_mybookmarks(self):
        headers = self.world.get('headers', dict())
        res = self.client.get('/api/bookmarks/', **headers)
        _world_response_status(self, res)

    def When_i_add_bookmark(self, pkg):
        postdata = dict(package_name=pkg.package_name)
        res = self.client.post('/api/bookmarks/', postdata)
        _world_response_status(self, res)

    def When_i_remove_bookmark(self, pkg):
        res = self.client.delete('/api/bookmarks/%d/' % pkg.pk)
        _world_response_status(self, res)

    def When_i_access_bookmark_check(self, pkg):
        res = self.client.head('/api/bookmarks/%d/' % pkg.pk)
        _world_response_status(self, res)

    def When_i_access_bookmarks_page(self):
        res = self.client.get('/api/bookmarks/')
        _world_response_status(self, res)

    def When_i_access_url_with_head_method(self, url):
        headers = self.world.get('headers', dict())
        res = self.client.head(url, **headers)
        _world_response_status(self, res)

    def When_i_post_package_update_versions(self, pkg_version_list):
        qs = json.dumps(dict(versions=pkg_version_list))
        res = self.client.post('/api/updates/',
                               content_type='application/json',
                               data=qs)
        _world_response_status(self, res)

    def Then_i_should_see_package_update_list_has_the_version(context,
                                                              package_name,
                                                              version_code,
                                                              version_name,
                                                              is_updatable):
        pkg_list = context.world.get('content')
        pkg_list | should | have(1).elements
        except_pkg = pkg_list[0]
        except_pkg['package_name'] | should | equal_to(package_name)
        except_pkg['version_code'] | should | equal_to(version_code)
        except_pkg['version_name'] | should | equal_to(version_name)
        except_pkg['is_updatable'] | should | equal_to(is_updatable)
        except_pkg | should | include_keys('download_size',
                                           'download',
                                           'icon',
                                           'title',
                                           'released_datetime')

    def When_i_access_comment_list(self, obj):

        serializer = PackageDetailSerializer(obj)
        res = self.client.get(serializer.data.get('comments_url'))
        _world_response_status(self, res)

    def When_i_post_comment_to(self, content, obj):
        from serializers import PackageDetailSerializer

        serializer = PackageDetailSerializer(obj)
        res = self.client.post(serializer.data.get('comments_url'),
                               dict(comment=content))
        _world_response_status(self, res)


    def When_i_access_my_commented_packages_page(self):
        res = self.client.get('/api/accounts/commented_packages',
                              follow=True)
        _world_response_status(self, res)

    def When_i_access_selfupdate(self):
        res = self.client.get('/api/selfupdate/')
        _world_response_status(self, res)

    def clear_world(self):
        self.world = {}

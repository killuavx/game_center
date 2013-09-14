# -*- encoding=utf-8 -*-
import io
from os.path import join, dirname, abspath
from django.test.testcases import TestCase
from django.test.client import Client
from django import forms
import json
from django.core.files import File
from warehouse.models import Package, Author, PackageVersion, PackageVersionScreenshot
from taxonomy.models import Category, Topic, TopicalItem
from django.utils.timezone import now, timedelta
import random
import logging
_models = []


def guid():
    def S4():
        return hex(int(((1 + random.random()) * 0x10000) or 0))[2:]
    return "%s%s-%s-%s-%s-%s%ss%s"%(S4(), S4(), S4(), S4(), S4(), S4(), S4(), S4())

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
    logging.info('create_topic', defaults)
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

def clear_data():
    for m in _models:
        try:  m.delete()
        except: pass

class ApiDSL(object):

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

    def Given_i_have_published_package(self, all_datetime, **kwargs):
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
                'screenshots',
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

    def Then_i_should_receive_success_response(self):
        response = self.world.get('response')
        self.assertEqual(response.status_code, 200)
        content = self.convert_content(response.content)
        self.world.update(dict(response=response, content=content))

    def Then_i_should_see_result_list(self, num, count=None, previous=None, next=None):
        content = self.world.get('content')
        count = num if count is None else count
        self.assertResultList(content=content,
                              previous=previous,
                              next=next,
                              count=count,
                              result_len=num )

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
            'package_name',
            'title',
            'released_datetime',
            'summary',
            'author',
        )
        for field in fields:
            self.assertIn(field, pkg_data)

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

    def When_i_access_package_detail(self, package):
        from warehouse.serializers import PackageSummarySerializer
        serializer = PackageSummarySerializer(package)
        repsonse = self.client.get(serializer.data.get('url'))
        self.world.update(dict(response=repsonse))

class RestApiTest(TestCase):

    def setUp(self):
        self.world = dict()
        self.client = Client(HTTP_ACCEPT='application/json',
                             HTTP_CACHE_CONTROL='no-cache')
        ApiDSL.setUp(self, client=self.client, world=self.world)

    def convert_content(self, content):
        return json.loads(content.decode('utf-8'))

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


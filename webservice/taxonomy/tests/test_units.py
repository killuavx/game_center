# -*- encoding=utf-8 -*-
from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings
from django.core.files import File
from django.utils.timezone import now, timedelta, localtime
from warehouse.models import Package, PackageVersion, Author
from tagging.models import Tag
from taxonomy.models import Category, Topic, TopicalItem
import io
import os
from os.path import join, abspath, dirname
from fts.tests import helpers
from fts.helpers import ApiDSL
import shutil
from should_dsl import should

_fixture_dir = join(dirname(abspath(__file__)), 'fixtures')
class BaseTestCase(TestCase):

    _fixture_dir = _fixture_dir

    _files_to_remove = []

    def setUp(self):
        _dir = join(self._fixture_dir, 'temp')
        os.makedirs(_dir, exist_ok=True)
        self._files_to_remove.append(_dir)
        super(BaseTestCase, self).setUp()

    def tearDown(self):
        for f in self._files_to_remove:
            shutil.rmtree(f, ignore_errors=True)
        helpers.clear_data()
        super(BaseTestCase, self).setUp()

    def assertIsSameTime(self, a, b):
        _a = a.replace(microsecond=0)
        _b = b.replace(microsecond=0)
        self.assertEqual(localtime(_a), localtime(_b))

class CategorySimpleTest(BaseTestCase):

    def _category(self, **defaults):
        return helpers.create_category(**defaults)

    def test_basic_creation(self):
        cat = Category(name="Test Case 1", slug='test-case-1')
        cat.save()
        except_cat = Category.objects.get(pk=cat.pk)
        self.assertEqual(except_cat.name, 'Test Case 1')
        self.assertEqual(except_cat.slug , 'test-case-1')
        except_cat.delete()

    def test_basic_creation_with_zhcn_and_slug_not_fill(self):
        cat = self._category(name="攻略")
        self.assertEqual(cat.name, '攻略')
        self.assertEqual(cat.slug, '攻略')
        cat2 = self._category(name="游戏", slug='game')
        except_cat2 = Category.objects.get(pk=cat2.pk)
        self.assertEqual(except_cat2.name, '游戏')
        self.assertEqual(except_cat2.slug , 'game')
        except_cat2.delete()

    def test_basic_creation_with_complex_world(self):
        cat = self._category(name="攻略 3")
        except_cat = Category.objects.get(pk=cat.pk)
        self.assertEqual(except_cat.slug, '攻略-3')
        except_cat.delete()

    def test_create_category_with_children(self):
        root = self._category(name="Game")
        rpg = self._category(name="RPG")
        root.children.add(rpg)
        except_root = Category.objects.get(pk=root.pk)
        self.assertEqual(except_root.children.count(), 1)
        self.assertEqual(except_root.children.get(), rpg)

    def test_create_category_with_parent(self):
        root = self._category(name="Game")
        rpg = self._category(name="RPG", parent=root)
        except_rpg = Category.objects.get(pk=rpg.pk)
        self.assertEqual(except_rpg.parent, root)
        self.assertEqual(except_rpg.children.count(), 0)

    @override_settings(MEDIA_ROOT=join(_fixture_dir, 'temp'))
    def test_upload_image_to_path(self):
        icon = io.FileIO(join(self._fixture_dir, 'category-icon.png'))
        cat = self._category(
            name="Game",
            icon=File(icon)
        )
        cat_icon_path = "category/%s/icon.png" % cat.slug
        cat.icon.path |should| end_with(cat_icon_path)

class CategoryWithPackageTest(BaseTestCase):

    def _category(self, **defaults):
        return helpers.create_category(**defaults)

    def _author(self):
        author = Author.objects.create(name="Kent Back")
        return author

    def _package(self):
        pkg = Package.objects.create(
            title="梦幻西游",
            package_name="com.menghuan.xiyou",
            author=self._author())
        return pkg

    def test_package_with_category_depth_1(self):
        pkg = self._package()
        cat = Category.objects.create(name="Game")
        pkg.categories.add(cat)

        self.assertEqual(cat.packages.get(), pkg)
        self.assertEqual(pkg.categories.get(), cat)

    def test_package_with_category_depth_2(self):
        pkg = self._package()
        game = self._category(name='Game')
        rpg = self._category(parent=game, name='RPG')
        pkg.categories.add(rpg)

        except_rpg = pkg.categories.get()
        self.assertEqual(except_rpg, rpg)
        self.assertEqual(except_rpg.parent, game)

    def test_package_with_mutil_category_depth_3(self):

        pkg = self._package()
        game = self._category(name="Game")
        rpg = self._category(parent=game, name='RPG')
        fps = self._category(parent=game, name="FPS")

        pkg.categories.add(rpg)
        pkg.categories.add(fps)

        except_cats = pkg.categories.all()
        self.assertEqual(len(except_cats), 2)
        except_rpg  = except_cats[0]
        except_fps  = except_cats[1]
        self.assertEqual(except_rpg, rpg)
        self.assertEqual(except_fps, fps)
        self.assertEqual(except_rpg.parent, game)
        self.assertEqual(except_fps.parent, game)

class TagTest(BaseTestCase):

    def test_basic_create(self):
        tag = Tag.objects.create(name="Hot")

        self.assertEqual(tag.name, 'Hot')
        tags = Tag.objects.all()
        self.assertEqual(len(tags), 1)

    def test_create_tags_with_package(self):
        pkg = helpers.create_package()
        pkg.tags_text = 'Hot, New'
        pkg.tags_text +=',Top'
        pkg.save()

        tags = Tag.objects.usage_for_model(model=pkg.__class__)
        self.assertEqual(len(tags), 3)
        self.assertEqual(tags[0].name, 'Hot')
        self.assertEqual(tags[1].name, 'New')
        self.assertEqual(tags[2].name, 'Top')

class TopcialSimpleTest(BaseTestCase):

    def test_manager_queryset(self):
        today = now() - timedelta(hours=1)
        biggame = Topic(name="大型游戏专区",
                        slug='big-game',
                        summary='big game, big play',
                        status=Topic.STATUS.published,
                        released_datetime=today)
        biggame.save()
        except_topic = Topic.objects.as_root().published().get()
        self.assertEqual(except_topic.name, biggame.name)

        except_topic_wiht_item_count =\
            Topic.objects.published().with_item_count().get()
        queryset = Topic.objects.as_root().published().with_item_count()
        self.assertEqual(0, except_topic_wiht_item_count.item_count)

    def test_basic_create(self):
        today = now() - timedelta(hours=1)
        biggame = Topic(name="大型游戏专区", slug='big-game',
                        summary='big game, big play',
                        released_datetime=today)
        biggame.cover = ApiDSL.Given_i_have_cover_image(self)
        biggame.icon = ApiDSL.Given_i_have_icon_image(self)
        biggame.save()

        except_biggame = Topic.objects.get()
        self.assertEqual(except_biggame.name, '大型游戏专区')
        self.assertEqual(except_biggame.slug, 'big-game')
        self.assertEqual(except_biggame.status, Topic.STATUS.draft)
        self.assertEqual(except_biggame.summary, 'big game, big play')
        self.assertIsSameTime(except_biggame.released_datetime, today)
        self.assertIsSameTime(except_biggame.updated_datetime,
                              today+timedelta(hours=1))
        self.assertIsSameTime(except_biggame.created_datetime,
                              today+timedelta(hours=1))

    def test_basic_create_with_some_package(self):
        today = now() - timedelta(hours=1)
        topic = ApiDSL.Given_i_have_topic_with(self,
                                       status=Topic.STATUS.published,
                                       all_datetime=today)
        package = ApiDSL.Given_i_have_package_with(self)
        version1 = ApiDSL.Given_package_has_version_with(self,
                    package, version_code=1, version_name='1.0',
                    all_datetime=today,
                    status=PackageVersion.STATUS.published)
        TopicalItem.objects.create(topic=topic, content_object=package)
        except_topic = package.topics.all()[0].topic

        self.assertEqual(except_topic.name, topic.name)
        self.assertEqual(except_topic.slug, topic.slug)

    @override_settings(MEDIA_ROOT=join(_fixture_dir, 'temp'))
    def test_upload_image_to_path(self):
        today = now() - timedelta(hours=1)
        icon = io.FileIO(join(self._fixture_dir, 'topic-icon.png'))
        cover = io.FileIO(join(self._fixture_dir, 'topic-cover.jpg'))
        biggame = Topic(name="大型游戏专区",
                        slug='big-game',
                        icon=File(icon),
                        cover=File(cover),
                        summary='big game, big play',
                        status=Topic.STATUS.published,
                        released_datetime=today)
        biggame.save()
        path = "topic/%s" % biggame.slug
        biggame.icon.path |should| end_with(join(path, 'icon.png'))
        biggame.cover.path |should| end_with(join(path, 'cover.jpg'))

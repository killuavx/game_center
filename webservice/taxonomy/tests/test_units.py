# -*- encoding=utf-8 -*-
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.timezone import now, timedelta, localtime
from tagging.models import Tag
from taxonomy.models import Category, Topic, TopicalItem
from fts.features.app_dsls import taxonomy, warehouse
import io
import os
from os.path import join, abspath, dirname
from fts import helpers
from fts.helpers import SubFile
import shutil
from should_dsl import should

_fixture_dir = join(dirname(abspath(__file__)), 'fixtures')


class TaxonomyBaseUnitTest(TestCase):

    tags = []

    world = {}

    _fixture_dir = _fixture_dir

    _files_to_remove = []

    def setUp(self):
        _dir = join(self._fixture_dir, 'temp')
        os.makedirs(_dir, exist_ok=True)
        self._files_to_remove.append(_dir)
        super(TaxonomyBaseUnitTest, self).setUp()
        self.WarehouseDSL = warehouse.factory_dsl(self)
        self.WarehouseDSL.setup(self)
        self.TaxonomyDSL = taxonomy.factory_dsl(self)
        self.TaxonomyDSL.setup(self)

    def tearDown(self):
        self.WarehouseDSL.teardown(self)
        self.TaxonomyDSL.teardown(self)

        for f in self._files_to_remove:
            shutil.rmtree(f, ignore_errors=True)
        super(TaxonomyBaseUnitTest, self).setUp()

        helpers.clear_data()

    def create_author(self, **kwargs):
        return self.WarehouseDSL.create_author_without_ui(self, **kwargs)

    def create_package(self, with_version=False, **kwargs):
        return self.WarehouseDSL.create_package_without_ui(
            self,
            with_version=with_version,
            **kwargs)

    def create_package_version(self, **kwargs):
        return self.WarehouseDSL.create_package_versions_without_ui(self,
                                                                    **kwargs)

    def create_screenshot(self, version):
        return self.WarehouseDSL.create_screenshot_without_ui(self, version)

    def create_category(self, **kwargs):
        return self.TaxonomyDSL.create_category(context=self, **kwargs)

    def create_topic(self, **kwargs):
        return self.TaxonomyDSL.create_topic(self, **kwargs)

    def assertIsSameTime(self, a, b):
        _a = a.replace(microsecond=0)
        _b = b.replace(microsecond=0)
        self.assertEqual(localtime(_a), localtime(_b))


class CategorySimpleTest(TaxonomyBaseUnitTest):

    def _category(self, **defaults):
        return helpers.create_category(**defaults)

    def test_basic_creation(self):
        cat = Category(name="Test Case 1", slug='test-case-1')
        cat.save()
        except_cat = Category.objects.get(pk=cat.pk)
        self.assertEqual(except_cat.name, 'Test Case 1')
        self.assertEqual(except_cat.slug, 'test-case-1')
        except_cat.delete()

    def test_basic_creation_with_zhcn_and_slug_not_fill(self):
        cat = self.create_category(name="攻略")
        self.assertEqual(cat.name, '攻略')
        self.assertEqual(cat.slug, '攻略')
        cat2 = self.create_category(name="游戏", slug='game')
        except_cat2 = Category.objects.get(pk=cat2.pk)
        self.assertEqual(except_cat2.name, '游戏')
        self.assertEqual(except_cat2.slug, 'game')
        except_cat2.delete()

    def test_basic_creation_with_complex_world(self):
        cat = self.create_category(name="攻略 3")
        except_cat = Category.objects.get(pk=cat.pk)
        self.assertEqual(except_cat.slug, '攻略-3')
        except_cat.delete()

    def test_create_category_with_children(self):
        root = self.create_category(name="Game")
        rpg = self.create_category(name="RPG")
        root.children.add(rpg)
        except_root = Category.objects.get(pk=root.pk)
        self.assertEqual(except_root.children.count(), 1)
        self.assertEqual(except_root.children.get(), rpg)

    def test_create_category_with_parent(self):
        root = self.create_category(name="Game")
        rpg = self.create_category(name="RPG", parent=root)
        except_rpg = Category.objects.get(pk=rpg.pk)
        self.assertEqual(except_rpg.parent, root)
        self.assertEqual(except_rpg.children.count(), 0)

    @override_settings(MEDIA_ROOT=join(_fixture_dir, 'temp'))
    def test_upload_image_to_path(self):
        icon = io.FileIO(join(self._fixture_dir, 'category-icon.png'))
        cat = self.create_category(
            name="Game",
            icon=SubFile.icon()
        )
        cat_icon_path = "category/%s/icon.png" % cat.slug
        cat.icon.path | should | end_with(cat_icon_path)


class CategoryWithPackageTest(TaxonomyBaseUnitTest):

    def _package(self):
        return self.create_package(
            title="梦幻西游",
            package_name="com.menghuan.xiyou",
        )

    def test_package_with_category_depth_1(self):
        pkg = self._package()
        cat = Category.objects.create(name="Game")
        pkg.categories.add(cat)

        self.assertEqual(cat.packages.get(), pkg)
        self.assertEqual(pkg.categories.get(), cat)

    def test_package_with_category_depth_2(self):
        pkg = self._package()
        game = self.create_category(name='Game')
        rpg = self.create_category(parent=game, name='RPG')
        pkg.categories.add(rpg)

        except_rpg = pkg.categories.get()
        self.assertEqual(except_rpg, rpg)
        self.assertEqual(except_rpg.parent, game)

    def test_package_with_mutil_category_depth_3(self):
        pkg = self._package()
        game = self.create_category(name="Game")
        rpg = self.create_category(parent=game, name='RPG')
        fps = self.create_category(parent=game, name="FPS")

        pkg.categories.add(rpg)
        pkg.categories.add(fps)

        except_cats = pkg.categories.all()
        self.assertEqual(len(except_cats), 2)
        except_rpg = except_cats[0]
        except_fps = except_cats[1]
        self.assertEqual(except_rpg, rpg)
        self.assertEqual(except_fps, fps)
        self.assertEqual(except_rpg.parent, game)
        self.assertEqual(except_fps.parent, game)


class TagTest(TaxonomyBaseUnitTest):

    def test_basic_create(self):
        tag = Tag.objects.create(name="Hot")

        self.assertEqual(tag.name, 'Hot')
        tags = Tag.objects.all()
        self.assertEqual(len(tags), 1)

    def test_create_tags_with_package(self):
        pkg = self.create_package(package_name="com.test")
        pkg.tags_text = 'Hot, New'
        pkg.tags_text += ',Top'
        pkg.save()

        tags = Tag.objects.usage_for_model(model=pkg.__class__)
        self.assertEqual(len(tags), 3)
        self.assertEqual(tags[0].name, 'Hot')
        self.assertEqual(tags[1].name, 'New')
        self.assertEqual(tags[2].name, 'Top')


class TopcialSimpleTest(TaxonomyBaseUnitTest):

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

        except_topic_wiht_item_count = \
            Topic.objects.published().with_item_count().get()
        queryset = Topic.objects.as_root().published().with_item_count()
        self.assertEqual(0, except_topic_wiht_item_count.item_count)

    def test_basic_create(self):
        today = now() - timedelta(hours=1)
        biggame = Topic(name="大型游戏专区", slug='big-game',
                        summary='big game, big play',
                        released_datetime=today)
        biggame.cover = SubFile.cover()
        biggame.icon = SubFile.icon()
        biggame.save()

        except_biggame = Topic.objects.get()
        self.assertEqual(except_biggame.name, '大型游戏专区')
        self.assertEqual(except_biggame.slug, 'big-game')
        self.assertEqual(except_biggame.status, Topic.STATUS.draft)
        self.assertEqual(except_biggame.summary, 'big game, big play')
        self.assertIsSameTime(except_biggame.released_datetime, today)
        self.assertIsSameTime(except_biggame.updated_datetime,
                              today + timedelta(hours=1))
        self.assertIsSameTime(except_biggame.created_datetime,
                              today + timedelta(hours=1))

    def test_basic_create_with_some_package(self):
        today = now() - timedelta(hours=1)
        topic = self.create_topic(name="test",
                                  status=Topic.STATUS.published,
                                  released_datetime=today,
                                  updated_datetime=today,
                                  created_datetime=today
        )
        package = self.create_package()
        version1 = self.create_package_version(
            package=package,
            version_code=1,
            version_name='1.0')
        TopicalItem.objects.create(topic=topic, content_object=package)
        except_topic = package.topics.all()[0].topic

        self.assertEqual(except_topic.name, topic.name)
        self.assertEqual(except_topic.slug, topic.slug)

    @override_settings(MEDIA_ROOT=join(_fixture_dir, 'temp'))
    def test_upload_image_to_path(self):
        today = now() - timedelta(hours=1)
        biggame = self.create_topic(
            name="大型游戏专区",
            slug='big-game',
            icon=SubFile.icon(),
            cover=SubFile.cover(),
            summary='big game, big play',
            status=Topic.STATUS.published,
            released_datetime=today,
            updated_datetime=today,
            created_datetime=today
        )
        biggame.save()
        path = "topic/%s" % biggame.slug
        biggame.icon.path | should | end_with(join(path, 'icon.png'))
        biggame.cover.path | should | end_with(join(path, 'cover.jpg'))

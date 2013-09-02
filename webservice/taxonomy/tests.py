# -*- encoding=utf-8 -*-
from django.test import TestCase
from warehouse.models import Package, Author
from taxonomy.models import Category

def create_category(**defaults):
    defaults.setdefault('name', "Kent Back")
    return Category.objects.create(**defaults)

class CategorySimpleTest(TestCase):

    def _category(self, **defaults):
        return create_category(**defaults)

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

class CategoryWithPackageTest(TestCase):

    def _category(self, **defaults):
        return create_category(**defaults)

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

def create_author(**defaults):
    defaults.setdefault('name', "Kent Back")
    return Author.objects.create(**defaults)

def create_package(**defaults):
    defaults.setdefault('title', "Kent Back")
    defaults.setdefault('package_name', "Kent Back")
    if not defaults.get('author'):
        defaults.setdefault('author', create_author())
    return Package.objects.create(**defaults)

from tagging.models import Tag
class TagTest(TestCase):

    def test_basic_create(self):
        tag = Tag.objects.create(name="Hot")

        self.assertEqual(tag.name, 'Hot')
        tags = Tag.objects.all()
        self.assertEqual(len(tags), 1)

    def test_create_tags_with_package(self):
        pkg = create_package()
        pkg.tags = 'Hot, New'
        pkg.tags +=',Top'
        pkg.save()

        tags = Tag.objects.usage_for_model(model=pkg.__class__)
        self.assertEqual(len(tags), 3)
        self.assertEqual(tags[0].name, 'Hot')
        self.assertEqual(tags[1].name, 'New')
        self.assertEqual(tags[2].name, 'Top')


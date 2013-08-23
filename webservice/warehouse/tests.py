# -*- encoding=utf-8 -*-
from django.test import TestCase
from warehouse.models import Package, Author, StatusNotSupportAction
from datetime import datetime , timedelta

class AuthorTest(TestCase):

    def test_basic_create(self):
        author = Author.objects.create(name="Martin Flower", 
                                       email="martin-flower@testcase.com")
        self.assertEqual(author.status, Author.STATUS.draft)

        except_author = Author.objects.get(pk=author.pk)
        self.assertEqual(except_author.name, "Martin Flower")
        self.assertEqual(except_author.email, "martin-flower@testcase.com")
        self.assertEqual(except_author.phone, None)
        
        self.assertEqual(str(author), "Martin Flower")
        
    def _create_author(self):
        author = Author.objects.create(name="Robort C. Martin",
                                       email="Uncle-Bob@testcase.com")
        return author
        
    def test_change_status_from_draft_to_unactivated(self):
        author = self._create_author()
        self.assertEqual(author.status, Author.STATUS.draft)
        author.review()
        self.assertEqual(author.status, Author.STATUS.unactivated)
        
    def test_change_status_from_unactivated_to_activated(self):
        author = self._create_author()
        author.status = Author.STATUS.unactivated
        self.assertEqual(author.status, Author.STATUS.unactivated)
        
        author.activate()
        self.assertEqual(author.status, Author.STATUS.activated)
        
    def test_change_status_from_activated_to_rejected(self):
        author = self._create_author()
        author.status = Author.STATUS.activated
        self.assertEqual(author.status, Author.STATUS.activated)

        author.reject()
        self.assertEqual(author.status, Author.STATUS.rejected)
        
    def test_change_status_from_rejected_to_activated(self):
        author = self._create_author()
        author.status = Author.STATUS.rejected
        self.assertEqual(author.status, Author.STATUS.rejected)
        
        author.appeal()
        self.assertEqual(author.status, Author.STATUS.unactivated)
        
    def test_change_status_from_rejected_to_draft(self):
        author = self._create_author()
        author.status = Author.STATUS.rejected
        self.assertEqual(author.status, Author.STATUS.rejected)

        author.recall()
        self.assertEqual(author.status, Author.STATUS.draft)

class PackageTest(TestCase):
    
    def setUp(self):
        self.author = Author.objects.create(name="Martin Flower", email="martin-flower@testcase.com")
    
    def test_basic_create(self):
        pkg = Package(title="谷歌地图", package_name="com.google.apps.map")
        pkg.author = self.author
        pkg.save()
        
        except_pkg = Package.objects.get(pk=pkg.pk)
        self.assertEqual(except_pkg.title, "谷歌地图")
        self.assertEqual(except_pkg.package_name, "com.google.apps.map")
        self.assertEqual(str(except_pkg), "谷歌地图")
        
        self.assertEqual(except_pkg.summary, "")
        self.assertEqual(except_pkg.description,"")
        
        # datetime compare with created_datetime, updated_datetime and released_time
        now = datetime.utcnow()
        self.assertEqual(except_pkg.released_datetime, None)
        created_timedelta = now - except_pkg.created_datetime.utcnow()
        self.assertLess(created_timedelta, timedelta(seconds=1))
        updated_timedelta = now - except_pkg.updated_datetime.utcnow()
        self.assertLess(updated_timedelta, timedelta(seconds=1))
        
        except_author = pkg.author
        self.assertEqual(except_author.name, "Martin Flower")
    
    def _create_with_one_version(self):
        pkg = Package(title="梦幻西游", package_name="com.menghuan.xiyou")
        pkg.author = self.author
        pkg.save()
        return Package.objects.get(pk=pkg.pk)
    
    def test_change_status_bewteen_draft_to_unpublished(self):
        pkg = self._create_with_one_version()
        self.assertEqual(pkg.status, Package.STATUS.draft)
        
        pkg.review()
        self.assertEqual(pkg.status, Package.STATUS.unpublished)
    
    def test_status_not_support_changed_between_unpublished_and_published(self):
        pkg = self._create_with_one_version()
        self.assertEqual(pkg.status, Package.STATUS.draft)

        pkg.review() # from Draft to Unpublished
        pkg.publish() # from Unpublished to published
        self.assertEqual(pkg.status, Package.STATUS.published)
        
        # Status Changed Not Support from Published to Unpublished
        with self.assertRaises(StatusNotSupportAction):
            pkg.unpublish()
        
    def test_change_status_between_unpublished_and_rejected(self):
        pkg = self._create_with_one_version()
        pkg.status = Package.STATUS.unpublished
        self.assertEqual(pkg.status, Package.STATUS.unpublished)
        
        pkg.reject() # from Unpublished to Rejected
        self.assertEqual(pkg.status, Package.STATUS.rejected)
        pkg.appeal() # from Rejected to Unpublished
        self.assertEqual(pkg.status, Package.STATUS.unpublished)
        
    def test_change_status_between_rejected_and_draft(self):
        pkg = self._create_with_one_version()
        pkg.status = Package.STATUS.rejected
        self.assertEqual(pkg.status, Package.STATUS.rejected)
        
        pkg.recall() # from Rejected to Draft
        self.assertEqual(pkg.status, Package.STATUS.draft)
        
    def test_change_status_between_published_and_reject(self):
        pkg = self._create_with_one_version()
        pkg.status = Package.STATUS.published
        self.assertEqual(pkg.status, Package.STATUS.published)
        
        pkg.reject()
        self.assertEqual(pkg.status, Package.STATUS.rejected)
        

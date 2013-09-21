# -*- encoding=utf-8 -*-
from django.test import TestCase
from warehouse.models import *
from datetime import datetime , timedelta
from fts.tests import helpers
from django.utils.timezone import now
from os.path import join, abspath, dirname

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
        return helpers.create_author(name="Robort C. Martin",
                                       email="Uncle-Bob@testcase.com")

    def test_change_status_from_draft_to_unactivated(self):
        author = self._create_author()
        self.assertEqual(author.status, Author.STATUS.draft)
        author.review()
        self.assertEqual(author.status, Author.STATUS.unactivated)
        
        author.save()
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
        self.author = helpers.create_author(name="Martin Flower", email="martin-flower@testcase.com")
    
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
        return helpers.create_package(title="梦幻西游",
                       package_name="com.menghuan.xiyou",
                       author=self.author)

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
    
    def test_status_draft_transactions_migration(self):
        pkg = self._create_with_one_version()
        self.assertEqual(pkg.status, Package.STATUS.draft)
        self.assertEqual(pkg.next_statuses,(Package.STATUS.unpublished,))
        self.assertEqual(pkg.next_actions,('review',))
        self.assertEqual(pkg.next_transactions(), 
                         ( ('review', Package.STATUS.unpublished), ))
        
    def test_status_unpublished_transactions_migration(self):
        pkg = self._create_with_one_version()
        pkg.status = Package.STATUS.unpublished
        self.assertEqual(pkg.status, Package.STATUS.unpublished)
        self.assertEqual(pkg.next_statuses,
                         (Package.STATUS.published, Package.STATUS.rejected))
        self.assertEqual(pkg.next_actions, ( 'publish', 'reject'))
        self.assertEqual(pkg.next_transactions(), (
                             ('publish', Package.STATUS.published),
                             ('reject' , Package.STATUS.rejected), ) 
                        )

    def test_status_rejected_transactions_migration(self):
        pkg = self._create_with_one_version()
        pkg.status = Package.STATUS.rejected
        self.assertEqual(pkg.status, Package.STATUS.rejected)

        self.assertEqual(pkg.next_statuses,
                         (Package.STATUS.draft, Package.STATUS.unpublished))
        self.assertEqual(pkg.next_actions, ('recall', 'appeal'))
        self.assertEqual(pkg.next_transactions(),(
            ('recall', Package.STATUS.draft),
            ('appeal', Package.STATUS.unpublished), )
        )
        
    def test_status_published_transaction_migration(self):
        pkg = self._create_with_one_version()
        pkg.status = Package.STATUS.published
        self.assertEqual(pkg.status, Package.STATUS.published)
        self.assertEqual(pkg.next_statuses, (Package.STATUS.rejected,))
        self.assertEqual(pkg.next_actions, ('reject',))
        self.assertEqual(pkg.next_transactions(), (
            ('reject', Package.STATUS.rejected) , )
        )

class PackageManagerTest(TestCase):

    _fixtures_dir = join(dirname(abspath(__file__)), 'fixtures')

    def setUp(self):
        super(PackageManagerTest, self).setUp()

    def test_package_version_has_many_screenshots(self):
        yestoday = now()-timedelta(days=1)
        pkg = self.Given_i_have_package_with(
            status=Package.STATUS.published,
            released_datetime=yestoday
        )
        version = ApiDSL.Given_package_has_version_with(self,
            pkg,
            version_code=1,
            version_name='1.0beta',
            all_datetime=yestoday,
            status=PackageVersion.STATUS.published
        )
        ApiDSL.Given_package_version_add_screenshot(self, version)

        except_pkg = Package.objects.get(pk=pkg.pk)
        except_version = except_pkg.versions.get()
        self.assertEqual(except_version.screenshots.count(), 1)
        except_ss = except_version.screenshots.get()
        self.assertIsNotNone(except_ss.image.url)
        except_ss.delete()

    def setUp(self):
        super(PackageManagerTest, self).setUp()
        self._count = 0

    def Given_i_have_package_with(self, status=None, released_datetime=None):
        self._count+=1
        pkg = helpers.create_package(package_name='com.gamecenter.%d' % self._count,
                                     title='游戏%d' % self._count,
                                     status=status,
                                     released_datetime=released_datetime
        )
        return pkg

    def test_published_list_should_all_status_ok(self):
        # tomorrow will be published
        tomorrow = now()+timedelta(days=1)
        self.Given_i_have_package_with(
                                  status=Package.STATUS.published,
                                  released_datetime=tomorrow
        )
        # yestoday published
        yestoday = now()-timedelta(days=1)
        self.Given_i_have_package_with(
                                  status=Package.STATUS.published,
                                  released_datetime=yestoday
        )
        # yestoday unpublished or else status
        self.Given_i_have_package_with(
                                  status=Package.STATUS.unpublished,
                                  released_datetime=yestoday
        )
        self.Given_i_have_package_with(
                                  released_datetime=yestoday,
                                  status=Package.STATUS.draft
        )
        published_pkgs_set = Package.objects.published()
        self.assertEqual(1, published_pkgs_set.count())

        pub_pkgs = published_pkgs_set.all()
        pkg = pub_pkgs[0]
        self.assertEqual(pkg.status, Package.STATUS.published)


from fts.tests.helpers import ApiDSL
class PackageVersionTest(TestCase):

    def setUp(self):
        super(PackageVersionTest, self).setUp()

    def test_basic_create(self):
        pkg = ApiDSL.Given_i_have_package_with(self,
            package_name='com.warehouse.tests.packageversion.%s' % helpers.guid(),
        )

        pkgversion = PackageVersion(
            version_name = '1.0beta',
            version_code = 1004,
            whatsnew = 'all new!'
        )
        pkg.versions.add(pkgversion)
        self.assertEqual(pkgversion.version_code, 1004)
        self.assertEqual(pkgversion.version_name, '1.0beta')
        self.assertEqual(pkgversion.whatsnew, 'all new!')

        except_pkgversion = Package.objects.get(pk=pkg.pk).versions.get()
        self.assertEqual(except_pkgversion, pkgversion)

    def test_should_package_with_version(self):
        pkg = ApiDSL.Given_i_have_package_with(self,
               package_name='com.warehouse.tests.packageversion.%s' % helpers.guid(),
        )
        version1 = PackageVersion(
            version_name = '1.0beta2',
            version_code = 1014,
            whatsnew = 'all new!'
        )
        version2 = PackageVersion(
            version_name = '1.0beta3',
            version_code = 1024,
            whatsnew = 'all new!'
        )
        pkg.versions.add(version1)
        pkg.versions.add(version2)

        except_pkg = Package.objects.get(pk=pkg.pk)
        self.assertEqual(except_pkg.versions.latest('version_code'), version2)

    def test_package_should_change_updated_datetime_sync_with_latest_published_version(self):
        yestoday = now() - timedelta(days=1)
        pkg = ApiDSL.Given_i_have_package_with(self,
               package_name='com.warehouse.tests.packageversion.%s' % helpers.guid(),
               released_datetime=yestoday,
               updated_datetime=yestoday,
               created_datetime=yestoday,
        )
        # published version at yestoday
        today = now() - timedelta(minutes=1)
        version1 = ApiDSL.Given_package_has_version_with(self, pkg,
                                                       all_datetime=yestoday ,
                                                       version_name='1.0beta', version_code=11010,
                                                       status=PackageVersion.STATUS.published)

        # new published version at today
        recently = today - timedelta(hours=2)
        version2 = ApiDSL.Given_package_has_version_with(self, pkg,
                                                       all_datetime=recently,
                                                       version_name='1.0beta2', version_code=11020,
                                                       status=PackageVersion.STATUS.draft)

        # package updated_datetime should be same with latest published version 1.0beta
        except_pkg = Package.objects.get(pk=pkg.pk)
        self.assertGreater( timedelta(seconds=1), version1.updated_datetime - except_pkg.updated_datetime)

    def test_package_should_change_updated_datetime_sync_with_latest_published_version_v2(self):
        yestoday = now() - timedelta(days=1)
        pkg = ApiDSL.Given_i_have_package_with(self,
                                               package_name='com.warehouse.tests.packageversion.%s' % helpers.guid(),
                                               released_datetime=yestoday,
                                               updated_datetime=yestoday,
                                               created_datetime=yestoday,
                                               )
        # published version at yestoday
        today = now() - timedelta(minutes=1)
        version1 = ApiDSL.Given_package_has_version_with(self, pkg,
                                      all_datetime=yestoday ,
                                       version_name='1.0beta', version_code=21010,
                                       status=PackageVersion.STATUS.published)

        # new published version at today
        recently = today - timedelta(hours=2)
        version2 = ApiDSL.Given_package_has_version_with(self, pkg,
                           all_datetime=recently,
                           version_name='1.0beta2', version_code=21020,
                           status=PackageVersion.STATUS.published)
        # package updated_datetime should be same with latest published version 1.0beta2
        except_pkg = Package.objects.get(pk=pkg.pk)
        self.assertGreater(timedelta(seconds=1), version2.updated_datetime - except_pkg.updated_datetime)


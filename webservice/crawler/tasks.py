# -*- coding: utf-8 -*-
import os
import xmlrpc.client
from dateutil.parser import parse as dateparse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import transaction, IntegrityError
from django.utils.timezone import now
from mongoengine import Q
from warehouse.models import *
from taxonomy.models import Category
from toolkit.fields import file_md5
from toolkit.models import Resource
from django.core.files import File
import io
from crawler.models import IOSAppData, IOSBuyInfo



def iosversion_upload_to_path(version, filename, newname=None):
    iospackage = version.package.iospackage
    return iosapp_upload_to_path(filename,
                                 newname=newname,
                                 appid=iospackage.track_id,
                                 version_code=version.version_code)


def iosapp_upload_to_path(filename, appid, version_code=1, newname=None):
    basename = os.path.basename(filename)
    if newname:
        name, extension = os.path.splitext(basename)
        params = dict()
        if '%(name)s' in newname:
            params['name'] = name
        if '%(extension)s' in newname:
            params['extension'] = extension.lstrip('.')
        basename = newname % params if params else newname

    path = "ipackage/%d/v%d" % (int(appid), version_code)
    return "%s/%s" %(path, basename)


def iosapp_buyinfo_path(filename, appid):
    basename = os.path.basename(filename)
    return "ipackage/%d/%s" % (int(appid), basename)


def unique_value(queryset, field, value, segment='-'):
    i = 0
    while True:
        if i > 0:
            if i > 1:
                value = value.rsplit(segment, 1)[0]
            value = "%s%s%s" % (value, segment, i)
        try:
            queryset.get(**{field: value})
        except ObjectDoesNotExist:
            break
        i += 1
    return value


def content_object_id(obj):
    ct = ContentType.objects.get_for_model(obj)
    content_type = str(ct.pk)
    object_pk = str(obj.pk)
    return content_type, object_pk


class BaseTask(object):

    def __init__(self):
        SITE_ID_IOS = 2
        os.environ.setdefault('MEZZANINE_SITE_ID', str(SITE_ID_IOS))

    def __del__(self):
        os.environ.pop('MEZZANINE_SITE_ID')


class TransformIOSAppDataToPackageVersionTask(BaseTask):

    def create_package(self, content_data, author):
        package_name = content_data['bundleId']
        released_datetime = dateparse(content_data['releaseDate'])
        track_id = content_data['trackId']
        package, created = IOSPackage.objects.get_or_create(
            track_id=track_id,
            defaults=dict(
                package_name=package_name,
                author=author,
                title=content_data['trackName'],
                description=content_data.get('description'),
                released_datetime=released_datetime,
                appleuser_rating=content_data.get('averageUserRating'),
                view_url=content_data['trackViewUrl'],
                status='unpublished',
            )
        )
        if created:
            categories = self.create_categories(content_data)
            for cat in categories:
                package.categories.add(cat)
        return package

    def create_author(self, content_data):
        artist_id = content_data['artistId']
        view_url = content_data.get('artistViewUrl')
        email = "%s@artistid.ccdev.com" % artist_id
        phone = artist_id

        try:
            author, created = IOSAuthor.objects.get_or_create(
                artist_id=artist_id,
                defaults=dict(
                    name=content_data['artistName'],
                    email=email,
                    phone=phone,
                    view_url=view_url,
                    seller_name=content_data.get('sellerName'),
                    seller_url=content_data.get('sellerUrl'),
                    status='unactivated',
                )
            )
        except IntegrityError:
            name = unique_value(IOSAuthor.objects.all(),
                                field='name',
                                value=content_data['artistName'],
                                segment=' - ')
            author, created = IOSAuthor.objects.get_or_create(
                name=name,
                defaults=dict(
                    artist_id=artist_id,
                    email=email,
                    phone=phone,
                    view_url=view_url,
                    seller_name=content_data.get('sellerName'),
                    seller_url=content_data.get('sellerUrl'),
                    status='unactivated',
                    )
            )

        return author

    def create_categories(self, content_data):
        cat_slug = content_data['wrapperType']
        kind = content_data['kind']
        genres = content_data['genres']
        genres.append(cat_slug)
        genre_ids = content_data['genreIds']
        primary_genre_id = content_data['primaryGenreId']
        primary_genre = content_data['primaryGenreName']
        genres.append(primary_genre)
        genres.append(kind)

        cats = list()
        for genre in genres:
            if not genre:
                continue
            cat, created = Category.objects.get_or_create(name=genre)
            cats.append(cat)
        return cats

    def create_packageversion(self, content_data, package):
        version_name = content_data['version']
        try:
            prev = package.versions.latest('version_code')
            version_code = prev.version_code + 1
        except ObjectDoesNotExist:
            version_code = 1

        devices = content_data.get('supportedDevices', list())
        is_support_iphone = any(dev.startswith('iPhone') for dev in devices)
        is_support_ipad = any(dev.startswith('iPad') for dev in devices)

        version, created = IOSPackageVersion.objects.get_or_create(
            package=package,
            version_name=version_name,
            version_code=version_code,
            defaults=dict(
                formatted_price=content_data.get('formattedPrice'),
                price=content_data.get('price', 0),
                price_currency=content_data.get('currency'),
                appleuser_rating=content_data.get('averageUserRatingForCurrentVersion'),
                appleformatted_rating=content_data.get('trackContentRating'),
                whatsnew=content_data.get('releaseNotes', ''),
                description=content_data.get('description'),
                status=IOSPackageVersion.STATUS.unpublished,
                is_support_iphone=is_support_iphone,
                is_support_ipad=is_support_ipad,
                released_datetime=package.released_datetime,
                )
            )

        # add supported
        languages = content_data.get('languageCodesISO2A', list())
        for lang in languages:
            supported_lang, created = SupportedLanguage.objects \
                .get_or_create(code=lang)
            version.supported_languages.add(supported_lang)

        devices = content_data.get('supportedDevices', list())
        for dev in devices:
            supported_dev, created = SupportedDevice.objects \
                .get_or_create(code=dev)
            version.supported_devices.add(supported_dev)

        features = content_data.get('features', list())
        for fea in features:
            supported_fea, created = SupportedFeature.objects \
                .get_or_create(code=fea)
            version.supported_features.add(supported_fea)

        return version

    def parse_app(self, app):
        content_data = app.content_data
        if not content_data:
            app.set_analysised(app.ANALYSIS_PACKAGEVERSION_EMPTY)
            app.save()
            return None

        sid = transaction.savepoint()
        try:
            author = self.create_author(content_data)
            package = self.create_package(content_data, author)
            version = self.create_packageversion(content_data, package)
            transaction.savepoint_commit(sid)
        except Exception as e:
            print(e)
            transaction.savepoint_rollback(sid)
        else:
            try:
                app.set_analysised(version)
                app.save()
            except IntegrityError:
                app.set_analysised(app.ANALYSIS_PACKAGEVERSION_DUPLICATION)
                app.save()


class DownloadIOSAppResourceTask(BaseTask):

    crawl_resource_doc_class = None

    def __init__(self, allow_overwrite=True):
        super(DownloadIOSAppResourceTask, self).__init__()
        from crawler.documents import CrawlResource
        self.crawl_resource_doc_class = CrawlResource
        self.allow_overwrite=allow_overwrite
        self.client = xmlrpc.client.ServerProxy("http://localhost:6800/rpc").aria2

    def _content_object_id(self, version):
        ct = ContentType.objects.get_for_model(version.__class__)
        content_type = str(ct.pk)
        object_pk = str(version.pk)
        return content_type, object_pk

    def download_app_resource(self, app):
        """
            下载一个app的资源
        """
        content_data = app.content_data
        if not content_data:
            return None
        resources = self.get_appdata_resources(app, content_data)

        content_type, object_pk = self._content_object_id(app)
        gids = []
        for item in resources:
            _gid = self._save_download_queue(item,
                                            content_type=content_type,
                                            object_pk=object_pk,
                                            )
            gids.append(_gid)
        return gids

    def get_appdata_resources(self, app, content_data):
        track_id = app.appid
        version_code = 1
        # [
        #   (url, save_to_relative_path, resource_type, file_alias), ...
        # ]
        download_resources = list()

        # icon
        for artwork_size in [60, 100, 512]:
            key = 'artworkUrl%s' %artwork_size
            if content_data.get(key):
                artwork_url = content_data[key]
                _file_uuid = artwork_url.split('/')[-2]
                _save_to = iosapp_upload_to_path(
                    filename=artwork_url,
                    appid=track_id,
                    version_code=version_code,
                    newname=os.path.join('icons', _file_uuid,
                                         '%(name)s.%(extension)s'))
                download_resources.append((artwork_url, _save_to, 'icon', key))

        # screenshot
        _cnt = 0
        for url in content_data['screenshotUrls']:
            _file_uuid = url.split('/')[-2]
            _save_to = iosapp_upload_to_path(
                filename=url,
                appid=track_id,
                version_code=version_code,
                newname=os.path.join('screenshots', _file_uuid, '%(name)s.%(extension)s'))
            download_resources.append((url, _save_to, 'screenshot', _cnt))
            _cnt += 1

        # ipad screenshot
        _cnt = 0
        for url in content_data['ipadScreenshotUrls']:
            _file_uuid = url.split('/')[-2]
            _save_to = iosapp_upload_to_path(
                filename=url,
                appid=track_id,
                version_code=version_code,
                newname=os.path.join('ipadscreenshots', _file_uuid, '%(name)s.%(extension)s'))
            download_resources.append((url, _save_to, 'ipadscreenshot', _cnt))
            _cnt += 1
        return download_resources

    def _save_download_queue(self, item, **kwargs):
        _file_path = os.path.join(settings.MEDIA_ROOT, item[1])
        _file_dir = os.path.dirname(_file_path)
        _id = self.client.addUri([item[0]], {'dir': _file_dir})
        url, relative_path, resource_type, file_alias = item
        try:
            self.crawl_resource_doc_class.objects.filter(
                relative_path=relative_path,
                **kwargs
            ).update_one(
                upsert=True,
                set__gid=_id,
                set__url=url,
                set__relative_path=relative_path,
                set__resource_type=resource_type,
                set__file_alias=str(file_alias),
                set__file_dir=_file_dir,
                set__file_path=_file_path,
            )
        except Exception as e:
            print(e)
        return _id

    def checkout_app_resources(self, app):
        """
           根据一个app，checkout app所有的资源
        """
        content_data = app.content_data
        if not content_data:
            return None

        qs = self.crawl_resource_doc_class.objects.by_content_object(app)
        for item in qs.filter(status__ne='complete'):
            try:
                self._update_resource_status_rpc(item)
            except (ConnectionRefusedError, xmlrpc.client.Fault) as e:
                self._update_resource_status_location(item)
            except Exception as e:
                print(e)

        try:
            version = app.packageversion
            is_published = qs.count() > 0 and all(i.status == 'complete' for i in qs)
            if is_published:
                version.status = IOSPackageVersion.STATUS.published
                version.save()
            app.is_image_downloaded = is_published
            app.image_downloaded = now()
            app.save()
        except ObjectDoesNotExist:
            pass
        self._msg_user_download_error(app)

    def _update_resource_status_location(self, item):
        item.updated = now()
        fname = os.path.join(settings.MEDIA_ROOT, item.relative_path)
        if os.path.isfile(fname):
            item.status = 'complete'
            item.file_size = os.path.getsize(fname)
        else:
            item.status = 'error'
            item.error_code = '1001'
        item.save()

    def _update_resource_status_rpc(self, item):
        tell_status = self.client.tellStatus(item.gid)
        item.status = tell_status['status']
        item.file_size = tell_status['completedLength']
        item.updated = now()
        item.save()
        self.client.removeDownloadResult(item.gid)

    def _msg_user_download_error(self, app):
        pass

    def update_app_status_check_resources(self, app):
        qs = self.crawl_resource_doc_class.objects.by_content_object(app)
        try:
            version = app.packageversion
            is_published = qs.count() > 0 and all(i.status == 'complete' for i in qs)
            if is_published:
                version.status = IOSPackageVersion.STATUS.published
                version.save()
            app.is_image_downloaded = is_published
            app.image_downloaded = now()
            app.save()
        except ObjectDoesNotExist:
            pass

    def checkout_each_resource(self):
        """
            checkout每个已经完成资源
        """
        qs = self.crawl_resource_doc_class.objects \
            .filter(Q(status__ne='complete') | Q(status__ne='waiting'))
        try:
            for item in qs:
                self._update_resource_status_rpc(item)
        except (ConnectionRefusedError, xmlrpc.client.Fault) as e:
            for item in qs:
                self._update_resource_status_location(item)
        except Exception as e:
            print(e)

    def retry_download_resource(self, status=None):
        """
           status in [ 'paused', 'error', 'active', 'posted' ]
        """
        qs = self.crawl_resource_doc_class.objects.all()
        if not status:
            qs = qs.filter(Q(status__ne='complete') | Q(status__ne='waiting'))
        else:
            qs = qs.filter(status=status)

        for item in qs:
            _id = self.client.addUri([item.url], {'dir': item.file_dir})
            item.gid = _id
            item.updated = now()
            item.status = 'retry'
            item.save()


class SyncIOSAppBuyInfoTask(BaseTask):

    def get_appdata(self, appid):
        qs = IOSAppData.objects.filter(appid=appid)
        return qs[0]

    def get_buyinfo_queryset(self):
        return IOSBuyInfo.objects.all()\
            .filter(buy_status=IOSBuyInfo.BUY_STATUS.ok).filter(ipafile_size=0)

    def sync_buyinfo(self, app, buyinfo):
        if not buyinfo.ipafile_name:
            return

        buyinfo.appdata = app
        buyinfo.ipafile = iosapp_buyinfo_path(buyinfo.ipafile_name, buyinfo.appid)
        buyinfo.ipafile_size = buyinfo.ipafile.size
        with io.FileIO(buyinfo.ipafile.path) as f:
            buyinfo.ipafile_md5 = file_md5(f)

        pn, buyinfo.version, buyinfo.short_version =\
            buyinfo.ipafile_name.rstrip('.ipa').split('_')
        buyinfo.updated = now()
        buyinfo.save()

    def do_sync(self, limit=None, start=None):
        qs = self.get_buyinfo_queryset()
        if limit and start:
            qs = qs[start:start+limit]
        elif limit:
            qs = qs[0:limit]

        for buyinfo in qs:
            print(buyinfo.appid, buyinfo.pk)
            try:
                appdata = self.get_appdata(buyinfo.appid)
            except (ObjectDoesNotExist, IndexError) as e:
                print(e)
                continue
            try:
                self.sync_buyinfo(appdata, buyinfo)
            except (FileExistsError, FileNotFoundError) as e:
                print(e)
                continue


class SyncIOSPackageVersionFromIOSAppBuyInfoTask(BaseTask):

    def get_buyinfo_queryset(self):
        return IOSBuyInfo.objects.all() \
            .filter(buy_status=IOSBuyInfo.BUY_STATUS.ok)\
            .filter(appdata__packageversion_id__gt=0) \
            .exclude(ipafile_size=0)

    def do_sync(self, limit=None, start=None):
        qs = self.get_buyinfo_queryset()
        if limit and start:
            qs = qs[start:start+limit]
        elif limit:
            qs = qs[0:limit]

        for buy in qs:
            version = buy.appdata.packageversion
            version.download = buy.ipafile
            version.status = version.STATUS.published
            version.save()
            print(version.pk)


class SyncIOSPackageVersionResourceFromCrawlResourceTask(BaseTask):

    crawl_resource_doc_class = None

    def __init__(self):
        super(SyncIOSPackageVersionResourceFromCrawlResourceTask, self).__init__()
        from crawler.documents import CrawlResource
        self.crawl_resource_doc_class = CrawlResource

    def get_crawl_resource_by(self, content_type, object_pk):
        return self.crawl_resource_doc_class.objects.filter(status='complete') \
            .filter(content_type=str(content_type)) \
            .filter(object_pk=str(object_pk)) \
            .filter(is_recorded__ne=True)

    def get_crawl_resource_objects(self, content_type):
        return self.crawl_resource_doc_class.objects.filter(status='complete') \
            .filter(content_type=str(content_type)) \
            .filter(is_recorded__ne=True)

    def get_appdata_queryset(self):
        return IOSAppData.objects.filter(is_image_downloaded=True,
                                         packageversion_id__gt=0).all()

    def do_sync(self, limit=None, start=None):
        qs = self.get_appdata_queryset()
        if limit and start:
            qs = qs[start:start+limit]
        elif limit:
            qs = qs[0:limit]

        ct = ContentType.objects.get_for_model(IOSAppData)
        content_type = str(ct.pk)
        for app in qs:
            print("===============%s===================" % app.pk)
            resources = self.get_crawl_resource_by(content_type=content_type,
                                                   object_pk=str(app.pk))
            for item in resources:
                try:
                    self.add_to_packageversion(item, app.packageversion)
                except (ObjectDoesNotExist, IntegrityError) as e:
                    print(e)
                    continue
                except Exception as e:
                    print(e)
                print(item.resource_type, item.relative_path)

    def add_to_packageversion(self, item, version):
        if not version:
            return
        version = IOSAppData.convert_normal_version(version)

        if item.resource_type in ('icon', 'screenshot', 'ipadscreenshot'):
            if item.resource_type == 'icon':
                alias = item.file_alias.replace('artworkUrl', '')
                self._update_icon(version, item)
            else:
                alias = item.file_alias

            if item.resource_type.endswith('screenshot'):
                self._upsert_screenshot(version, item)

            res = self._upsert_resource(version, item, alias)

            item.is_recorded = True
            item.resource_id = res.pk
            item.save()

    def _update_icon(self, version, item):
        fname = os.path.join(settings.MEDIA_ROOT, item.relative_path)
        version.icon = item.relative_path
        version.save()

    def _upsert_screenshot(self, version, item):
        kind = 'default' if item.resource_type == 'screenshot' else 'ipad'
        screenshot, created = version.screenshots.get_or_create(kind=kind,
                                          image=item.relative_path)
        return screenshot

    def _upsert_resource(self, version, item, alias):
        resource = Resource(
            kind=item.resource_type,
            alias=alias,
            content_object=version,
            file=item.relative_path
        )
        try:
            version.resources.add(resource)
        except IntegrityError as e:
            print(e)
        return resource

    def sync_resourcefiles_to_version(self, app):
        """
            同步已下载的资源文件到PackageVersion上
        """
        if not app.packageversion:
            return None

        version = IOSAppData.convert_normal_version(app.packageversion)

        ct = ContentType.objects.get_for_model(IOSAppData)
        crawl_resources = self.get_crawl_resource_by(ct.pk, app.pk)
        for crawl_res in crawl_resources:
            self.add_to_packageversion(crawl_res, version)

        return True

    def get_appdata(self, pk):
        return IOSAppData.objects.get(pk=int(pk))

    def do_sync_by_crawl_resource_item(self, limit=None, start=None):
        ct = ContentType.objects.get_for_model(IOSAppData)
        qs = self.get_crawl_resource_objects(content_type=ct.pk)
        if limit and start:
            qs = qs[start:start+limit]
        elif limit:
            qs = qs[0:limit]

        for item in qs:
            print("======%s:%s=======" % (item.content_type, item.object_pk ))
            try:
                app = self.get_appdata(item.object_pk)
                self.add_to_packageversion(item, app.packageversion)
            except (ObjectDoesNotExist, IntegrityError) as e:
                print(e)
                continue
            print(item.resource_type, item.relative_path)


import json
import os
from dateutil.parser import parse as dateparse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from taxonomy.models import Category
from warehouse.models import (
    SupportedDevice,
    SupportedFeature,
    SupportedLanguage,
    IOSAuthor,
    IOSPackage,
    IOSPackageVersion,
    PackageVersion)


class IOSAppData(models.Model):

    appid = models.CharField(max_length=100, db_index=True)

    package_name = models.CharField(max_length=200, null=True, blank=True)

    version_name = models.CharField(max_length=200, null=True, blank=True)

    mainclass = models.CharField(max_length=50, db_index=True)

    subclass = models.CharField(max_length=50, db_index=True)

    device = models.IntegerField()

    is_free = models.IntegerField(db_column='isfree')

    is_analysised = models.BooleanField()

    content = models.TextField(db_column='download_content')

    packageversion_id = models.IntegerField(db_index=True,
                                            null=True, blank=True)

    def _get_packageversion(self):
        if self.packageversion_id:
            return IOSPackageVersion.objects.get(pk=self.packageversion_id)
        return None

    def _set_packageversion(self, packageversion):
        if isinstance(packageversion, int):
            packageversion = IOSPackageVersion.objects.get(pk=packageversion)
            self.packageversion_id = packageversion.pk
        elif isinstance(packageversion, IOSPackageVersion):
            self.packageversion_id = packageversion.pk
        elif isinstance(packageversion, PackageVersion):
            try:
                iospackageversion = packageversion.iospackageversion
                self.packageversion_id = iospackageversion.pk
            except ObjectDoesNotExist:
                raise TypeError('version must instance of IOSPackageVersion: %s' % packageversion)
        else:
            raise TypeError('version must instance of IOSPackageVersion')

    packageversion = property(_get_packageversion, _set_packageversion)

    class Meta:
        index_together = (
            ('mainclass', 'subclass'),
        )
        unique_together = (
            ('appid', 'package_name', 'version_name'),
        )

    def _get_content_json(self):
        if not hasattr(self, '_content_data'):
            try:
                content = json.loads(self.content)['results'][0]
            except:
                content = None
            self._content_data = content
        return self._content_data
    content_data = property(_get_content_json)

import xmlrpc.client


rpc_client = xmlrpc.client.ServerProxy("http://localhost:6800/rpc")


def iosversion_upload_to_path(version, filename, newname=None):
    basename = os.path.basename(filename)
    if newname:
        name, extension = os.path.splitext(basename)
        params = dict()
        if '%(name)s' in newname:
            params['name'] = name
        if '%(extension)s' in newname:
            params['extension'] = extension.lstrip('.')
        basename = newname % params if params else newname

    iospackage = version.package.iospackage

    path = "ipackage/%d/v%d" % (iospackage.track_id, version.version_code)
    return "%s/%s" %(path, basename)


class TransformIOSAppDataToPackageVersion(object):

    client = rpc_client.aria2

    crawler_resource_doc_class = None

    def __init__(self):
        SITE_ID_IOS = 2
        os.environ.setdefault('MEZZANINE_SITE_ID', str(SITE_ID_IOS))
        from crawler.documents import CrawlResource
        self.crawl_resource_doc_class = CrawlResource

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
        view_url = content_data['artistViewUrl']
        email = "%s@artistid.ccdev.com" % artist_id
        phone = artist_id
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

    def get_appdata_resources(self, content_data, version):
        download_resources = list()
        for artwork_size in [60, 100, 512]:
            key = 'artworkUrl%s' %artwork_size
            if content_data.get(key):
                artwork_url = content_data[key]
                _file_uuid = artwork_url.split('/')[-2]
                _save_to = iosversion_upload_to_path(
                    version,
                    artwork_url,
                    os.path.join('icons',
                                  _file_uuid,
                                  '%(name)s.%(extension)s'))
                download_resources.append((artwork_url, _save_to, 'icon', key))

        _cnt = 0
        for url in content_data['screenshotUrls']:
            _file_uuid = url.split('/')[-2]
            _save_to = iosversion_upload_to_path(
                version,
                url,
                os.path.join('screenshots', _file_uuid, '%(name)s.%(extension)s'))
            download_resources.append((url, _save_to, 'screenshot', _cnt))
            _cnt += 1

        _cnt = 0
        for url in content_data['ipadScreenshotUrls']:
            _file_uuid = url.split('/')[-2]
            _save_to = iosversion_upload_to_path(
                version,
                url,
                os.path.join('ipadscreenshots', _file_uuid, '%(name)s.%(extension)s'))
            download_resources.append((url, _save_to, 'ipadscreenshot', _cnt))
            _cnt += 1
        return download_resources

    def _content_object_id(self, version):
        ct = ContentType.objects.get_for_model(version.__class__)
        content_type = str(ct.pk)
        object_pk = str(version.pk)
        return content_type, object_pk

    def download_remote_resources(self, version, resources):
        for item in resources:
            content_type, object_pk = self._content_object_id(version)
            self.save_download_queue(item,
                                     content_type=content_type,
                                     object_pk=object_pk,
                                     )

    def save_download_queue(self, item, **kwargs):
        _file_path = os.path.join(settings.MEDIA_ROOT, item[1])
        _file_dir = os.path.dirname(_file_path)
        _id = self.client.addUri([item[0]], {'dir': _file_dir})
        try:
            self.crawl_resource_doc_class(
                gid=_id,
                url=item[0],
                relative_path=item[1],
                resource_type=item[2],
                file_alias=str(item[3]),
                file_dir=_file_dir,
                file_path=_file_path,
                **kwargs).save()
        except Exception as e:
            print(e)

    def parse_app(self, app):
        content_data = app.content_data
        if not content_data:
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
            app.packageversion = version
            app.package_name = version.package.package_name
            app.version_name = version.version_name
            app.save()

    def parse_app_resource(self, app):
        content_data = app.content_data
        if not content_data:
            return None
        version = app.packageversion
        resources = self.get_appdata_resources(content_data, version)
        self.download_remote_resources(version, resources)

    def checkout_app_resource(self, app):
        content_data = app.content_data
        if not content_data:
            return None
        version = app.packageversion
        try:
            self._crawl_resource_status_rpc(version)
        except (ConnectionRefusedError, xmlrpc.client.Fault) as e:
            self._crawl_resource_status_location(version)
        self._msg_user_download_error(version)
        self._update_version_status(version)

    def _msg_user_download_error(self, version):
        pass

    def _update_version_status(self, version):
        qs = self.crawl_resource_doc_class.objects \
            .by_content_object(version)
        is_published = all(i.status == 'complete' for i in qs)
        if is_published:
            version.status = IOSPackageVersion.STATUS.published
            version.save()

    def _crawl_resource_status_location(self, version):
        qs = self.crawl_resource_doc_class.objects \
            .by_content_object(version).filter(status__ne='complete')
        for item in qs:
            self._update_resource_status_location(item)

    def _update_resource_status_location(self, item):
        item.updated = now()
        if os.path.isfile(item.file_path):
            item.status = 'complete'
            item.file_size = os.path.getsize(item.file_path)
        else:
            item.status = 'error'
            item.error_code = '1001'
        item.save()

    def _crawl_resource_status_rpc(self, version):
        qs = self.crawl_resource_doc_class.objects\
            .by_content_object(version).filter(status__ne='complete')
        for item in qs:
            try:
                self._update_resource_status_rpc(item)
            except (ConnectionRefusedError, xmlrpc.client.Fault) as e:
                raise e
            except Exception as e:
                print(e)

    def _update_resource_status_rpc(self, item):
        tell_status = self.client.tellStatus(item.gid)
        item.status = tell_status['status']
        item.file_size = tell_status['completedLength']
        item.updated = now()
        item.save()
        self.client.removeDownloadResult(item.gid)

    def checkout_each_resource(self):
        qs = self.crawl_resource_doc_class.objects \
            .filter(status__ne='complete')
        try:
            for item in qs:
                self._update_resource_status_rpc(item)
        except (ConnectionRefusedError, xmlrpc.client.Fault) as e:
            for item in qs:
                self._update_resource_status_location(item)
        except Exception as e:
            print(e)


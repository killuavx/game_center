# -*- coding: utf-8 -*-
from celery import app
from django.db import models
from toolkit.helpers import set_global_site_id, SITE_NOT_SET
import warehouse.documents as doc
from warehouse.models import Package, PackageVersion
from searcher.search_indexes import PackageSearchIndex

import logging
logger = logging.getLogger('scripts')

TASK_OK = 0

TASK_ABORT = 100

TASK_ABORT_OBJECT_NOT_EXIST = 101

TASK_ABORT_STATUS_NOT_PUBLISHED = 102

TASK_ABORT_OBJECT_NOT_MATCH = 103


def delete_package_data_center(package_id):
    handler = doc.SyncPackageDocumentHandler()
    handler.delete(package_id)
    try:
        psi = PackageSearchIndex()
        package = Package.all_objects.get(pk=package_id)
        psi.remove_object(package)
        package.invalidate_tagging_cache()
    except:
        pass
    return TASK_OK


@app.shared_task(name='warehouse.tasks.publish_packageversion')
def publish_packageversion(version_id):
    """
    新发布package version, 同步Package.released_datetime/status
    """
    try:
        version = PackageVersion.all_objects.get(pk=version_id)
    except PackageVersion.DoesNotExist:
        return TASK_ABORT_OBJECT_NOT_EXIST

    def _task_process():
        # 1. version状态未发布则不处理
        if version.status != PackageVersion.STATUS.published:
            return TASK_ABORT_STATUS_NOT_PUBLISHED

        package = version.package
        published_versions = package.versions.published(released_hourly=False)

        # 2. version不是最后可发布的版本，则不处理
        try:
            expect_version = published_versions.latest('version_code')
            if expect_version.pk != version.pk:
                return TASK_ABORT_OBJECT_NOT_MATCH
        except PackageVersion.DoesNotExist:
            # 3. 没有最后可发布版本
            return TASK_ABORT_OBJECT_NOT_MATCH

        package.latest_version = version
        _sync_version_status(package, version, status=Package.STATUS.published)
        _sync_package_download_count(package)
        package.save()
        return TASK_OK

    set_global_site_id(version.site_id)
    task_result = _task_process()

    package = version.package
    search_index = PackageSearchIndex()
    handler = doc.SyncPackageDocumentHandler()
    if task_result == TASK_OK:
        try:
            handler.all_sync(package, version)
            search_index.update_object(package)
            # invalidate tagging cache
            package.invalidate_tagging_cache()
            package.latest_version.invalidate_tagging_cache()
            # build object cache
            Package.all_objects.get_cache_by(package.pk)
            PackageVersion.all_objects.get_cache_by(package.latest_version_id)
        except:
            task_result = TASK_ABORT
        else:
            task_result = TASK_OK
    elif task_result == TASK_ABORT_OBJECT_NOT_MATCH:
        delete_package_data_center(version.package_id)

    set_global_site_id(SITE_NOT_SET)
    return task_result


def _sync_version_status(package, version, status):
    if status == package.STATUS.published:
        package.released_datetime = version.released_datetime
    package.status = status
    package.has_award = version.has_award
    package.award_coin = version.award_coin


def _sync_package_download_count(package):
    aggregate = package.versions.published(released_hourly=False) \
        .aggregate(download_count=models.Sum('download_count'))
    total_count = aggregate.get('download_count', 0)
    package.download_count = total_count if total_count else 0


@app.shared_task(name='warehouse.tasks.unpublish_packageversion_from_published')
def unpublish_packageversion_from_published(version_id):
    """
    将已经发布的package version设置为未发布
    """
    try:
        version = PackageVersion.all_objects.get(pk=version_id)
    except PackageVersion.DoesNotExist:
        return TASK_ABORT_OBJECT_NOT_EXIST

    if version.status != PackageVersion.STATUS.published:
        return TASK_ABORT_STATUS_NOT_PUBLISHED

    set_global_site_id(version.site_id)
    def _task_process():
        package = version.package
        # 1. 只有一个版本直接设置 unpublished
        if package.versions.all().count() == 1:
            _sync_version_status(package, version,
                                 status=Package.STATUS.unpublished)
            _sync_package_download_count(package)
            package.save()
            return TASK_OK

        published_versions = package.versions.published(released_hourly=False)

        # 2. version 并不是最后发布的版本，不处理
        try:
            expect_version = published_versions.latest('version_code')
            if expect_version.pk != version.pk:
                return TASK_OK
        except PackageVersion.DoesNotExist:
            pass

        # 3. version的上一个published状态的版本, 设置Package.released_datetime与上一版本一致
        try:
            latest_second_version = published_versions \
                .exclude(version_code=version.version_code).latest('version_code')
            _sync_version_status(package, latest_second_version,
                                 status=Package.STATUS.published)
            _sync_package_download_count(package)
            package.save()
        except PackageVersion.DoesNotExist:
            # 4. 都没有已发布版本，将Package.status设置为unpublished
            package.status = Package.STATUS.unpublished
            package.save()
            return TASK_OK

        return TASK_OK

    task_result = _task_process()
    delete_package_data_center(version.package_id)
    set_global_site_id(SITE_NOT_SET)

    return task_result


@app.shared_task(name='warehouse.tasks.sync_package')
def sync_package(package_id):
    try:
        package = Package.all_objects.get(pk=package_id)
    except Package.DoesNotExist:
        return TASK_ABORT_OBJECT_NOT_MATCH

    task_result = TASK_OK
    set_global_site_id(package.site_id)
    if package.is_published() and package.latest_version:
        search_index = PackageSearchIndex()
        handler = doc.SyncPackageDocumentHandler()
        try:
            handler.all_sync(package, package.latest_version)
            search_index.update_object(package)

            # invalidate tagging cache
            package.invalidate_tagging_cache()
            package.latest_version.invalidate_tagging_cache()
            # build object cache
            Package.all_objects.get_cache_by(package.pk)
            PackageVersion.all_objects.get_cache_by(package.latest_version_id)

        except:
            task_result = TASK_ABORT
    else:
        task_result = TASK_ABORT_STATUS_NOT_PUBLISHED

    set_global_site_id(SITE_NOT_SET)
    return task_result



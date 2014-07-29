# -*- coding: utf-8 -*-
from celery import app
from django.db import models
from dateutil import parser as dateparser
from django.utils.timezone import now, make_aware, is_aware, get_default_timezone

import logging
logger = logging.getLogger('scripts')

TASK_OK = 0

TASK_ABORT = 100

TASK_ABORT_OBJECT_NOT_EXIST = 101

TASK_ABORT_STATUS_NOT_PUBLISHED = 102

TASK_ABORT_OBJECT_NOT_MATCH = 103


@app.shared_task(name='warehouse.tasks.publish_packageversion')
def publish_packageversion(version_id):
    """
    新发布package version, 同步Package.released_datetime/status
    """
    from warehouse.models import Package, PackageVersion
    try:
        version = PackageVersion.objects.get(pk=version_id)
    except PackageVersion.DoesNotExist:
        return TASK_ABORT_OBJECT_NOT_EXIST

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

    _sync_version_status(package, version, status=Package.STATUS.published)
    _sync_package_download_count(package)
    package.save()
    return TASK_OK


def _sync_version_status(package, version, status):
    if status == package.STATUS.published:
        package.released_datetime = version.released_datetime
    package.status = status


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
    from warehouse.models import Package, PackageVersion
    try:
        version = PackageVersion.objects.get(pk=version_id)
    except PackageVersion.DoesNotExist:
        return TASK_ABORT_OBJECT_NOT_EXIST

    if version.status != PackageVersion.STATUS.published:
        return TASK_ABORT_STATUS_NOT_PUBLISHED

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
        latest_second_version = published_versions\
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


# -*- coding: utf-8 -*-
from django.core.exceptions import MultipleObjectsReturned
from warehouse.models import *
from toolkit.helpers import SITE_ANDROID, SITE_IOS, SITE_NOT_SET, set_global_site_id

PLATFORM_ANDROID = 'android'
PLATFORM_IOS = 'ios'


def set_platfrom(device_platform_dim):
    if isinstance(device_platform_dim, str):
        platform = device_platform_dim
    else:
        platform = device_platform_dim.platform

    if platform == PLATFORM_ANDROID:
        set_global_site_id(site_id=SITE_ANDROID)
        return True
    elif platform == PLATFORM_IOS:
        set_global_site_id(site_id=SITE_IOS)
        return True
    else:
        return False


def unset_platform():
    set_global_site_id(SITE_NOT_SET)


def find_platform_package_version(device_platform_dim, package_dim):
    if not set_platfrom(device_platform_dim):
        return None
    try:
        p = Package.objects.get(package_name=package_dim.package_name)
    except Package.DoesNotExist:
        unset_platform()
        return None

    try:
        v = p.versions.get(version_name=package_dim.version_name)
    except MultipleObjectsReturned:
        v = p.versions.filter(version_name=package_dim.version_name).latest('version_code')
    except PackageVersion.DoesNotExist:
        v = None
    unset_platform()
    return p, v


def find_platform_package(device_platform_dim, packagekey_dim):
    if not set_platfrom(device_platform_dim):
        return None
    try:
        p = Package.objects.get(package_name=packagekey_dim.package_name)
    except Package.DoesNotExist:
        p = None
    unset_platform()
    return p


def find_platform_categories(device_platform_dim, packagekey_dim):
    set_platfrom(device_platform_dim)
    try:
        p = Package.objects.get(package_name=packagekey_dim.package_name)
    except Package.DoesNotExist:
        unset_platform()
        return None

    second_category_slugs = ('crack-game', )
    primary_category = None
    second_category = None
    root_category = None
    for c in p.main_categories:
        if c.slug in second_category_slugs:
            second_category = c
        else:
            if not primary_category:
                primary_category = c
    if not primary_category:
        primary_category = second_category
    if primary_category:
        root_category = primary_category.get_root()

    unset_platform()
    return root_category, primary_category, second_category


def packageversion_id_fill(package_dim):
    pv = find_platform_package_version(package_dim.platform, package_dim)
    if pv:
        pkg, version = pv
        if pkg:
            package_dim.title = pkg.title
            package_dim.pid = pkg.pk
        package_dim.vid = version.pk if version else None
    return package_dim



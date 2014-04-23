# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.managers import CurrentSiteManager as DjangoCSM
from model_utils.managers import PassThroughManager


def current_site_id():
    """
        0. combine
        1. android
        2. ios
    """
    from mezzanine.utils.sites import current_site_id as _cur_site_id
    site_id = _cur_site_id()
    if site_id == 3:
        return 1
    return site_id


def current_site():
    from mezzanine.utils.sites import current_site_id as _cur_site_id
    from django.contrib.sites.models import Site
    site_id = _cur_site_id()
    return Site.objects.get(pk=site_id)


def current_request():
    from mezzanine.core.request import current_request as _cur_request
    return _cur_request()


class CurrentSiteManager(DjangoCSM):
    """
    Extends Django's site manager to first look up site by ID stored in
    the request, the session, then domain for the current request
    (accessible via threadlocals in ``mezzanine.core.request``), the
    environment variable ``MEZZANINE_SITE_ID`` (which can be used by
    management commands with the ``--site`` arg, finally falling back
    to ``settings.SITE_ID`` if none of those match a site.
    """
    def __init__(self, field_name=None, *args, **kwargs):
        super(DjangoCSM, self).__init__(*args, **kwargs)
        self.__field_name = field_name
        self.__is_validated = False

    def get_query_set(self):
        if not self.__is_validated:
            self._validate_field_name()
        lookup = {self.__field_name + "__id__exact": current_site_id()}
        return super(DjangoCSM, self).get_query_set().filter(**lookup)


class CurrentSitePassThroughManager(CurrentSiteManager,
                                    PassThroughManager):
    pass


class SiteRelated(models.Model):

    class Meta:
        abstract = True

    site = models.ForeignKey("sites.Site", db_index=True, editable=False)

    def save(self, update_site=False, *args, **kwargs):
        """
        Set the site to the current site when the record is first
        created, or the ``update_site`` argument is explicitly set
        to ``True``.
        """
        if update_site or not self.id:
            self.site_id = current_site_id()
        super(SiteRelated, self).save(*args, **kwargs)


class MultiSiteRelated(models.Model):

    class Meta:
        abstract = True

    sites = models.ManyToManyField("sites.Site", null=True, blank=True)


class CurrentSiteInMultiSiteRelatedManager(DjangoCSM):

    def __init__(self, field_name=None, *args, **kwargs):
        super(DjangoCSM, self).__init__(*args, **kwargs)
        self.__field_name = field_name
        self.__is_validated = False

    def get_query_set(self):
        if not self.__is_validated:
            self._validate_field_name()
        ids = [current_site_id()]
        if 0 not in ids:
            ids.append(0)
        lookup = {self.__field_name + "__id__in": ids}
        return super(DjangoCSM, self).get_query_set().filter(**lookup)

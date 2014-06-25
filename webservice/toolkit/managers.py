# -*- coding: utf-8 -*-
import os
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.managers import CurrentSiteManager as DjangoCSM
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import get_models, Q, Manager
from django.db.models.query import QuerySet
from django.utils.encoding import force_text
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import PassThroughManager, PassThroughManagerMixin
from toolkit.helpers import get_global_site, released_hourly_datetime


class PublishedManager(Manager):
    """
    Provides filter for restricting items returned by status and
    publish date when the given user is not a staff member.
    """

    def published(self, for_user=None, released_hourly=True):
        """
        For non-staff users, return items with a published status and
        whose publish and expiry dates fall before and after the
        current date when specified.
        """
        dt = released_hourly_datetime(now(), released_hourly)

        from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
        if for_user is not None and for_user.is_staff:
            return self.all()
        return self.filter(
            Q(publish_date__lte=dt) | Q(publish_date__isnull=True),
            Q(expiry_date__gte=dt) | Q(expiry_date__isnull=True),
            Q(status=CONTENT_STATUS_PUBLISHED))

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

    def url_map(self, for_user=None, **kwargs):
        """
        Returns a dictionary of urls mapped to Displayable subclass
        instances, including a fake homepage instance if none exists.
        Used in ``mezzanine.core.sitemaps``.
        """
        from mezzanine.utils.urls import home_slug
        home = self.model(title=_("Home"))
        setattr(home, "get_absolute_url", home_slug)
        items = {home.get_absolute_url(): home}
        for model in get_models():
            if issubclass(model, self.model):
                for item in (model.objects.published(for_user=for_user)
                             .filter(**kwargs)
                             .exclude(slug__startswith="http://")
                             .exclude(slug__startswith="https://")):
                    items[item.get_absolute_url()] = item
        return items


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
        site = get_global_site()
        if not site:
            return super(DjangoCSM, self).get_query_set()

        if not self.__is_validated:
            self._validate_field_name()
        lookup = {self.__field_name + "__id__exact": site.pk}
        return super(DjangoCSM, self).get_query_set().filter(**lookup)


class CurrentSitePassThroughManager(PassThroughManagerMixin,
                                    CurrentSiteManager):
    pass


class ResourceManager(PassThroughManagerMixin, CurrentSiteManager):
    """
        get Resource from model
        obj.resources.{kind}.{alias}
    """

    def for_model(self, model):
        """
        QuerySet for all for a particular model (either an instance or
        a class).
        """
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_query_set().filter(content_type=ct)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_text(model._get_pk_val()))
        return qs

    def __getattr__(self, kind):
        if 'model' not in self.__dict__:
            raise AttributeError('%s has not attribute %s' % (self.__class__, kind))
        resource_model = self.__dict__['model']
        if kind not in resource_model.KIND:
            raise AttributeError('%s not in %s' % (kind, resource_model.KIND))
        kind_resources = self.filter(kind=kind)

        class FilterKindDict(dict):

            def count(self):
                return kind_resources.count()

            def __getattr__(self, alias):
                return kind_resources.get(alias=alias)

            def __getitem__(self, alias):
                if isinstance(alias, int):
                    return kind_resources[alias]
                return kind_resources.get(alias=alias)

            def __iter__(self):
                return kind_resources

            def __repr__(self):
                return '<FilterKindDict: %s>' % kind

        return FilterKindDict()


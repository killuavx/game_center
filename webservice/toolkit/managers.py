# -*- coding: utf-8 -*-
from django.contrib.sites.managers import CurrentSiteManager as DjangoCSM, CurrentSiteManager
from django.db.models import get_models, Q, Manager
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import PassThroughManager
from toolkit.models import current_site_id


class PublishedManager(Manager):
    """
    Provides filter for restricting items returned by status and
    publish date when the given user is not a staff member.
    """

    def published(self, for_user=None):
        """
        For non-staff users, return items with a published status and
        whose publish and expiry dates fall before and after the
        current date when specified.
        """
        from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
        if for_user is not None and for_user.is_staff:
            return self.all()
        return self.filter(
            Q(publish_date__lte=now()) | Q(publish_date__isnull=True),
            Q(expiry_date__gte=now()) | Q(expiry_date__isnull=True),
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
        if not self.__is_validated:
            self._validate_field_name()
        lookup = {self.__field_name + "__id__exact": current_site_id()}
        return super(DjangoCSM, self).get_query_set().filter(**lookup)


class CurrentSitePassThroughManager(CurrentSiteManager,
                                    PassThroughManager):
    pass



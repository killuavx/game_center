# -*- coding: utf-8 -*-
from toolkit import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models
from django.contrib.sites.managers import CurrentSiteManager as DjangoCSM
from mezzanine.utils.models import get_user_model_name
from model_utils.managers import PassThroughManager
from django.utils.translation import ugettext_lazy as _


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


class Star(models.Model):
    """
    A rating that can be given to a piece of content.
    """

    by_comment = models.OneToOneField("generic.ThreadedComment",
                                      related_name='content_star',
                                      default=None,
                                      null=True,
                                      blank=True)

    value = models.IntegerField(_("Value"))
    rating_date = models.DateTimeField(_("Rating date"),
                                       auto_now_add=True, null=True)
    content_type = models.ForeignKey("contenttypes.ContentType", related_name='+')
    object_pk = models.IntegerField()
    content_object = GenericForeignKey("content_type", "object_pk")
    user = models.ForeignKey(get_user_model_name(), verbose_name=_("Rater"),
                             null=True, related_name="%(class)ss")

    def __str__(self):
        return 'rating for %s' % (self.content_object)

    class Meta:
        db_table = 'common_star'
        verbose_name = _("Star")
        verbose_name_plural = _("Stars")

    def save(self, *args, **kwargs):
        """
        Validate that the rating falls between the min and max values.
        """
        valid = map(str, settings.STARS_RANGE)
        if str(self.value) not in valid:
            raise ValueError("Invalid rating. %s is not in %s" % (self.value,
                                                                  ", ".join(valid)))
        super(Star, self).save(*args, **kwargs)


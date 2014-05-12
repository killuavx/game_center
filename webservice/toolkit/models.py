# -*- coding: utf-8 -*-
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models
from mezzanine.utils.models import get_user_model_name, base_concrete_model
from django.utils.translation import ugettext_lazy as _
from toolkit import settings


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
    return int(site_id)


def current_site():
    from mezzanine.utils.sites import current_site_id as _cur_site_id
    from django.contrib.sites.models import Site
    site_id = _cur_site_id()
    return Site.objects.get(pk=site_id)


def current_request():
    from mezzanine.core.request import current_request as _cur_request
    return _cur_request()


CONTENT_STATUS_DRAFT = 1
CONTENT_STATUS_PUBLISHED = 2
CONTENT_STATUS_CHOICES = (
    (CONTENT_STATUS_DRAFT, _("Draft")),
    (CONTENT_STATUS_PUBLISHED, _("Published")),
)


class PublishDisplayable(models.Model):
    """
    Abstract model that provides features of a visible page on the
    website such as publishing fields. Basis of Mezzanine pages,
    blog posts, and Cartridge products.
    """

    status = models.IntegerField(_("Status"),
                                 choices=CONTENT_STATUS_CHOICES, default=CONTENT_STATUS_PUBLISHED,
                                 help_text=_("With Draft chosen, will only be shown for admin users "
                                             "on the site."))
    publish_date = models.DateTimeField(_("Published from"),
                                        help_text=_("With Published chosen, won't be shown until this time"),
                                        blank=True, null=True)
    expiry_date = models.DateTimeField(_("Expires on"),
                                       help_text=_("With Published chosen, won't be shown after this time"),
                                       blank=True, null=True)
    short_url = models.URLField(blank=True, null=True)
    in_sitemap = models.BooleanField(_("Show in sitemap"), default=True)

    search_fields = {"keywords": 10, "title": 5}

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Set default for ``publish_date``. We can't use ``auto_now_add`` on
        the field as it will be blank when a blog post is created from
        the quick blog form in the admin dashboard.
        """
        if self.publish_date is None:
            self.publish_date = now()
        super(PublishDisplayable, self).save(*args, **kwargs)

    def get_admin_url(self):
        from mezzanine.utils.urls import admin_url
        return admin_url(self, "change", self.id)

    def publish_date_since(self):
        """
        Returns the time since ``publish_date``.
        """
        return timesince(self.publish_date)
    publish_date_since.short_description = _("Published from")

    def get_absolute_url(self):
        """
        Raise an error if called on a subclass without
        ``get_absolute_url`` defined, to ensure all search results
        contains a URL.
        """
        name = self.__class__.__name__
        raise NotImplementedError("The model %s does not have "
                                  "get_absolute_url defined" % name)

    def _get_next_or_previous_by_publish_date(self, is_next, **kwargs):
        """
        Retrieves next or previous object by publish date. We implement
        our own version instead of Django's so we can hook into the
        published manager and concrete subclasses.
        """
        arg = "publish_date__gt" if is_next else "publish_date__lt"
        order = "publish_date" if is_next else "-publish_date"
        lookup = {arg: self.publish_date}
        concrete_model = base_concrete_model(PublishDisplayable, self)
        try:
            queryset = concrete_model.objects.published
        except AttributeError:
            queryset = concrete_model.objects.all
        try:
            return queryset(**kwargs).filter(**lookup).order_by(order)[0]
        except IndexError:
            pass

    def get_next_by_publish_date(self, **kwargs):
        """
        Retrieves next object by publish date.
        """
        return self._get_next_or_previous_by_publish_date(True, **kwargs)

    def get_previous_by_publish_date(self, **kwargs):
        """
        Retrieves previous object by publish date.
        """
        return self._get_next_or_previous_by_publish_date(False, **kwargs)


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

    by_comment = models.ForeignKey('generic.ThreadedComment',
                                   default=None,
                                   null=True,
                                   blank=True,
                                   related_name='content_star',
                                   on_delete=models.DO_NOTHING
                                   )

    value = models.IntegerField(_("Value"))
    rating_date = models.DateTimeField(_("Rating date"),
                                       auto_now_add=True, null=True)
    content_type = models.ForeignKey("contenttypes.ContentType",
                                     related_name='+')
    object_pk = models.IntegerField()
    content_object = GenericForeignKey("content_type", "object_pk")

    user = models.ForeignKey(get_user_model_name(),
                             verbose_name=_("Rater"),
                             default=True,
                             null=True, blank=True,
                             related_name="%(class)ss",
                             on_delete=models.DO_NOTHING
                             )

    ip_address = models.IPAddressField(blank=True,
                                       null=True)

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


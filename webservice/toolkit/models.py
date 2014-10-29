# -*- coding: utf-8 -*-
import io
from os.path import join
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models
from mezzanine.utils.models import get_user_model_name, base_concrete_model
from django.utils.translation import ugettext_lazy as _
from django.core.files.images import ImageFile
from model_utils import FieldTracker
from model_utils.choices import Choices

from django.conf import settings as df_settings
from toolkit import settings
from toolkit.managers import ResourceManager
from toolkit.fields import FileField
from toolkit.helpers import file_md5, current_site_id


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


import mimetypes
mimetypes.init(["pythonclub.org-mimetypes.txt"])


def resource_upload_path(instance, filename):
    if hasattr(instance.content_object, 'workspace'):
        prefix = instance.content_object.workspace.name
    else:
        prefix = 'temps/%s' % now().strftime('%Y%m%d')
    return join(prefix, instance.kind, filename)


class Resource(SiteRelated, models.Model):

    objects = ResourceManager()

    content_type = models.ForeignKey("contenttypes.ContentType", related_name='+')
    object_pk = models.IntegerField()
    content_object = GenericForeignKey("content_type", "object_pk")

    KIND = Choices(
        ('icon', 'icon', 'Icon'),
        ('cover', 'cover', 'Cover'),
        ('screenshot', 'screenshot', 'Screenshot'),
        ('ipadscreenshot', 'ipadscreenshot', 'iPadScreenshot'),
        ('other', 'other', 'Other'),
        ('pkg', 'pkg', 'PackageFile'),
    )

    kind = models.CharField(choices=KIND, max_length=15)

    alias = models.CharField(default='default', blank=True, max_length=50)

    alt = models.CharField(max_length=100, default='', blank=True)

    file = FileField(max_length=500,
                     upload_to='temps')

    # file check
    mime_type = models.CharField(max_length=100, default=None, null=True, blank=True)

    file_md5 = models.CharField(max_length=40, default=None, null=True, blank=True)

    file_size = models.IntegerField(default=0, blank=True)

    width = models.CharField(max_length=6, default=0, blank=True)

    height = models.CharField(max_length=6, default=0, blank=True)

    tracker = FieldTracker()

    class Meta:
        db_table = 'common_resource'
        index_together = (
            ('site', 'content_type', ),
            ('site', 'content_type', 'object_pk',),
            ('site', 'content_type', 'object_pk', 'kind'),
        )
        unique_together = (
            ('site', 'content_type', 'object_pk', 'kind', 'alias'),
        )
        ordering = ('site', 'content_type', 'object_pk', 'kind')

    def check_file_meta(self):
        if self.file.exists():
            self.file_size = self.file.filesize

            filepath = join(df_settings.MEDIA_ROOT, self.file.name)
            with io.FileIO(filepath) as f:
                self.file_md5 = file_md5(f)

                if self.mime_type and self.mime_type.startswith('image'):
                    image_file = ImageFile(f)
                    self.height, self.width = image_file.height, image_file.width

    def save(self, update_meta=False, *args, **kwargs):
        self.mime_type, _ext = mimetypes.guess_type(self.file.name)
        if update_meta or (self.kind == self.KIND.pkg and self.tracker.has_changed('file')):
            self.check_file_meta()
        return super(Resource, self).save(*args, **kwargs)

    def __str__(self):
        return "%s,%s:[%s]" % (self.kind, self.alias, self.file.name)



# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from mptt.models import MPTTModel, TreeForeignKey

from easy_thumbnails.fields import ThumbnailerImageField
from django.db.models import SlugField

from django.core.urlresolvers import get_callable
from django.conf import settings

slugify_function_path = getattr(settings, 'SLUGFIELD_SLUGIFY_FUNCTION', 'taxonomy.helpers.slugify')
slugify = get_callable(slugify_function_path)

class Taxonomy(models.Model):
    name = models.CharField(max_length=32,
                            unique=True,
                            help_text='Short descriptive name for this taxonomy.',
                            )


    slug = SlugField(max_length=32,
                     blank=False,
                     unique=True,
                     db_index=True,
                     help_text='Short descriptive unique name for use in urls.',
                     )

    ordering = models.PositiveIntegerField(
        max_length=4,
        db_index=True,
        blank=True,
        default=0
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.slug:
            self.slug = slugify(self.name)

        return super(Taxonomy, self).save(force_insert=False,
                                          force_update=False,
                                          using=None,
                                          update_fields=None)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Category(MPTTModel, Taxonomy):

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        left_attr = 'mptt_lft'
        right_attr = 'mptt_rgt'
        level_attr = 'mptt_level'

    subtitle = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default='',
        help_text='Some titles may be the same and cause confusion in admin '
                  'UI. A subtitle makes a distinction.',
        )
    icon = ThumbnailerImageField(
        resize_source=dict(size=(50, 50), crop='smart'),
        upload_to='icons',
        blank=True)

    @models.permalink
    def get_absolute_url(self):
        return reverse('category_object_list', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('name',)
        verbose_name = _('category')
        verbose_name_plural = _('categories')


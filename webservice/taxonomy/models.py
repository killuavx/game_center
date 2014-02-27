# -*- coding: utf-8 -*-
from django.utils.timezone import now
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.query import QuerySet
from model_utils import Choices, FieldTracker
from model_utils.fields import StatusField
from model_utils.managers import PassThroughManager
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from easy_thumbnails.fields import ThumbnailerImageField
from django.db.models import SlugField

from django.core.urlresolvers import get_callable
from django.conf import settings

slugify_function_path = getattr(settings, 'SLUGFIELD_SLUGIFY_FUNCTION',
                                'taxonomy.helpers.slugify')
slugify = get_callable(slugify_function_path)


def factory_taxonomy_upload_to_path(basename):
    def update_to(instance, filename):
        extension = filename.split('.')[-1].lower()
        path = "%(prefix)s/%(slug)s/%(filename)s.%(extension)s" % {
            'prefix': str(instance.__class__.__name__).lower(),
            'slug': instance.slug,
            'filename': basename,
            'extension': extension
        }
        return path

    return update_to


class Taxonomy(models.Model):
    name = models.CharField(max_length=32,
                            unique=True,
                            help_text=_(
                                'Short descriptive name for this taxonomy.'),
    )

    slug = SlugField(
        max_length=32,
        blank=False,
        unique=True,
        db_index=True,
        help_text=_('Short descriptive unique name for use in urls.'),
    )

    ordering = models.PositiveIntegerField(
        default=0,
        blank=True,
        db_index=True)

    is_hidden = models.BooleanField(
        default=False,
        blank=True,
        help_text=_('can visit from font side but hidden'))

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


class CategoryQuerySet(QuerySet):
    def as_root(self):
        return self.filter(parent=None)

    def published(self):
        return self

    def by_parent(self, category):
        return self.filter(parent__pk=category.pk)

    def by_parent_pk(self, category_pk):
        return self.filter(parent__pk=category_pk)

    def with_item_count(self):
        return self.annotate(item_count=models.Count('packages'))

    def hidden(self, flag=None):
        if flag is None:
            return self
        elif flag:
            return self.filter(is_hidden=True)
        else:
            return self.filter(is_hidden=False)

    def showed(self):
        return self.hidden(False)


class CategoryManager(TreeManager, PassThroughManager):
    pass


class Category(MPTTModel, Taxonomy):
    objects = CategoryManager.for_queryset_class(CategoryQuerySet)()

    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')

    class MPTTMeta:
        left_attr = 'mptt_lft'
        right_attr = 'mptt_rgt'
        level_attr = 'mptt_level'
        order_insertion_by = ['ordering']

    class Meta:
        ordering = ('ordering',)
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    subtitle = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default='',
        help_text='Some titles may be the same and cause confusion in admin '
                  'UI. A subtitle makes a distinction.',
    )

    icon = ThumbnailerImageField(
        default='',
        upload_to=factory_taxonomy_upload_to_path('icon'),
        blank=True
    )

    @models.permalink
    def get_absolute_url(self):
        return ('category_package_list', (), dict(slug=self.slug))

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        Category.objects.rebuild()


class TopicQuerySet(QuerySet):
    def as_root(self):
        return self.filter(parent=None)

    def published(self):
        return self.filter(
            released_datetime__lte=now(),
            status=str(self.model.STATUS.published))

    def by_parent(self, topic):
        return self.filter(parent__pk=topic.pk)

    def by_parent_pk(self, topic_pk):
        return self.filter(parent__pk=topic_pk)

    def with_item_count(self):
        return self.annotate(item_count=models.Count('items'))

    def hidden(self, flag=None):
        if flag is None:
            return self
        elif flag:
            return self.filter(is_hidden=True)
        else:
            return self.filter(is_hidden=False)

    def showed(self):
        return self.hidden(False)

    def by_ordering(self):
        return self.order_by('ordering')


class TopicManager(TreeManager, PassThroughManager):
    pass


class Topic(MPTTModel, Taxonomy):
    objects = TopicManager.for_queryset_class(TopicQuerySet)()

    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')

    class MPTTMeta:
        left_attr = 'mptt_lft'
        right_attr = 'mptt_rgt'
        level_attr = 'mptt_level'
        order_insertion_by = ['ordering']

    class Meta:
        ordering = ('ordering',)
        verbose_name = _('topic')
        verbose_name_plural = _('topics')

    icon = ThumbnailerImageField(
        verbose_name=_('icon image'),
        default='',
        upload_to=factory_taxonomy_upload_to_path('icon'),
        blank=True,
    )

    cover = ThumbnailerImageField(
        verbose_name=_('cover image'),
        default='',
        upload_to=factory_taxonomy_upload_to_path('cover'),
        blank=True,
    )

    summary = models.CharField(
        verbose_name=_('summary'),
        max_length=255,
        null=False,
        default="",
        blank=True
    )

    tracker = FieldTracker()

    STATUS = Choices(
        ('draft', _('Draft')),
        ('unpublished', _('Unpublished')),
        ('published', _('Published')),
    )

    status = StatusField(default='draft', blank=True)

    released_datetime = models.DateTimeField(blank=True,
                                             null=True,
                                             db_index=True)

    updated_datetime = models.DateTimeField(db_index=True,
                                            editable=False)

    created_datetime = models.DateTimeField(editable=False)

    def is_published(self):
        return self.status == self.STATUS.published \
            and self.released_datetime <= now()

    def save(self, *args, **kwargs):
        super(Topic, self).save(*args, **kwargs)
        Topic.objects.rebuild()

    @models.permalink
    def get_absolute_url(self):
        return ('topic_package_list', (), dict(slug=self.slug))


class TopicalItemQuerySet(QuerySet):
    def get_items_by_topic(self, topic, item_model):
        content_type = ContentType.objects.get_for_model(item_model)
        return item_model.objects \
            .filter(topics__topic__pk=topic.pk,
                    topics__content_type__pk=content_type.pk) \
            .order_by('topics__ordering')


class TopicalItem(models.Model):
    objects = PassThroughManager.for_queryset_class(TopicalItemQuerySet)()

    topic = models.ForeignKey(Topic, related_name='items')

    content_type = models.ForeignKey(ContentType,
                                     related_name='topic_content_type')
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey("content_type", "object_id")

    ordering = models.PositiveIntegerField(default=0, blank=True, db_index=True)

    updated_datetime = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        unique_together = (('topic', 'content_type', 'object_id'),)
        index_together = (('topic', 'content_type'), )
        ordering = ('ordering', )
        verbose_name = _('topical item')
        verbose_name_plural = _('topical items')

    def __str__(self):
        return '%s [%s]' % (self.content_object, self.topic)


from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Topic)
def topic_pre_save(sender, instance, **kwargs):
    """same with DatetimeField(auto_now=True),
    but model datetime changed by custom with auto_now=True would be overwrite on save action
    """
    changed = instance.tracker.changed()
    try:
        changed.pop('updated_datetime')
    except KeyError:
        pass

    if len(changed) \
        and not instance.tracker.has_changed('updated_datetime'):
        instance.updated_datetime = now()

    if not instance.created_datetime:
        instance.created_datetime = now()

    if instance.tracker.has_changed('status') \
        and instance.status == sender.STATUS.published \
        and not instance.released_datetime:
        instance.released_datetime = now()



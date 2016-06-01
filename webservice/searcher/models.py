from django.db import models
from django.db.models.query import QuerySet
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices, FieldTracker
from model_utils.fields import StatusField
from model_utils.managers import PassThroughManager
from toolkit.helpers import released_hourly_datetime
from toolkit.managers import CurrentSitePassThroughManager
from toolkit.models import SiteRelated


class TipsWordQuerySet(QuerySet):

    def order_weight(self):
        return self.order_by('-weight')

    def order_random(self):
        return self.order_by('?')

    def between_weight(self, start, end):
        return self.filter(weight__range=(start, end))

    def published(self, released_hourly=True):
        dt = released_hourly_datetime(now(), released_hourly)
        return self.filter(
            released_datetime__lte=dt, status=self.model.STATUS.published)


class TipsWord(SiteRelated, models.Model):

    objects = CurrentSitePassThroughManager\
        .for_queryset_class(TipsWordQuerySet)()

    keyword = models.CharField(_('keyword'),
                               max_length=36)

    weight = models.PositiveIntegerField(_('ordering weight'),
                                         max_length=8,
                                         default=0,
                                         blank=True)

    STATUS = Choices(
        ('draft', _('Draft')),
        ('reject', _('Reject')),
        ('unpublished', _('Unpublished')),
        ('published', _('Published')),
    )

    status = StatusField(verbose_name=_('status'),
                         default=STATUS.draft,
                         blank=True)

    released_datetime = models.DateTimeField(blank=True,
                                             null=True,
                                             db_index=True)

    updated_datetime = models.DateTimeField(db_index=True)

    created_datetime = models.DateTimeField()

    tracker = FieldTracker()

    def __str__(self):
        return str(self.keyword)

    class Meta:
        verbose_name = _("tips word ")
        verbose_name_plural = _("tips words")
        ordering = ('-weight',)
        unique_together = (
            ('site', 'keyword'),
        )

from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=TipsWord)
def tipsword_pre_save(sender, instance, **kwargs):
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


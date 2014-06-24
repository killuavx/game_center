from django.db import models
from model_utils.managers import PassThroughManager
from mezzanine.core.managers import DisplayableManager
from mezzanine.core.models import Displayable, Orderable, TimeStamped

from toolkit import model_url_mixin as urlmixin
from toolkit.helpers import current_site_id
from toolkit.managers import (CurrentSitePassThroughManager,
                              PublishedManager,
                              CurrentSiteManager,)
from toolkit.models import (
    SiteRelated,
    PublishDisplayable)

#from django.utils.translation import ugettext_lazy as _


class PackageRankingTypeManager(CurrentSitePassThroughManager,
                                DisplayableManager):
    pass


class PackageRankingType(Displayable):

    objects = PackageRankingTypeManager()

    def save(self, update_site=False, *args, **kwargs):
        if update_site or not self.id:
            self.site_id = current_site_id()
        super(PackageRankingType, self).save(update_site=False, *args, **kwargs)

    def get_absolute_url(self):
        return '#'

    class Meta:
        verbose_name = '榜单类型'
        verbose_name_plural = '榜单类型列表'
        unique_together = (
            ('site', 'slug',)
        )
        index_together = (
            ('publish_date', ),
            ('expiry_date', ),
            ('status', ),
            ('site', 'status', 'publish_date', 'expiry_date')
        )
        ordering = ('site', 'status', 'publish_date', 'expiry_date')


class PackageRankingManager(PublishedManager,
                            CurrentSiteManager,
                            PassThroughManager):
    pass


class PackageRanking(SiteRelated,
                     PublishDisplayable,
                     TimeStamped,
                     Orderable,
                     urlmixin.PackageRankingAbsoluteUrlMixin,
                     models.Model):

    objects = PackageRankingManager()

    CYCLE_TYPES = (
        (0, 'all'),
        (1, 'daily'),
        (2, 'weekly'),
        (3, 'monthly'),
        (4, '3days'),
        (5, 'custom'),
    )

    cycle_type = models.IntegerField(choices=CYCLE_TYPES,
                                     verbose_name='周期',
                                     default=0)

    ranking_type = models.ForeignKey(PackageRankingType, verbose_name='类型')

    category = models.ForeignKey('taxonomy.Category',
                                 verbose_name='应用分类',
                                 default=None,
                                 null=True,
                                 blank=True,
                                 limit_choices_to=dict(
                                     site_id=current_site_id,
                                 )
                                 )

    packages = models.ManyToManyField('warehouse.Package',
                                    symmetrical=False,
                                    through='PackageRankingItem',
                                    related_name='rankings',
                                    blank=True,
                                    null=True,
                                    limit_choices_to=dict(
                                        ranking_rankingitems__package__site_id=current_site_id
                                    )
                                    )
    @property
    def title(self):
        return self.ranking_type.title

    @property
    def slug(self):
        return self.ranking_type.slug

    def get_slug(self):
        return self.ranking_type.slug

    class Meta:
        verbose_name = '榜单'
        verbose_name_plural = '榜单列表'
        index_together = (
            ('site', 'category'),
            ('site', 'category', '_order'),
            ('site', 'category', 'cycle_type'),
            ('site', 'category', 'ranking_type'),
            ('site', 'status', 'publish_date', 'expiry_date'),
            ('site', 'in_sitemap'),
        )
        unique_together = (
            ('site', 'category', 'ranking_type', 'cycle_type', ),
        )

        ordering = ('site', '_order')


class PackageRankingItem(Orderable,
                         TimeStamped,
                         models.Model):

    ranking = models.ForeignKey(PackageRanking,
                                related_name='ranking_rankingitems',
                                limit_choices_to=dict(
                                    site_id=current_site_id
                                )
                                )
    package = models.ForeignKey('warehouse.Package',
                                related_name='ranking_rankingitems',
                                limit_choices_to=dict(
                                    site_id=current_site_id
                                ),
                                )

    class Meta:
        verbose_name = '榜单应用'
        verbose_name_plural = '榜单应用列表'
        unique_together = (
            ('ranking', 'package',)
        )
        index_together =(
            ('ranking', '_order'),
            ('ranking', 'package'),
        )
        ordering = ('ranking', '_order', )

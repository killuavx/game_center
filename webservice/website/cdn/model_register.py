# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_save
from .core import Feedback
from .errors import WorkingDirectoryNotFound
from .processors.warehouse import PackageVersionProcessor
from .processors.taxonomy import TopicProcessor, CategoryProcessor
from .processors.promotion import AdvertisementProcessor
from .processors.clientapp import ClientPackageVersionProcessor, LoadingCoverProcessor
from warehouse.models import PackageVersion
from promotion.models import Advertisement
from taxonomy.models import Category, Topic
from clientapp.models import ClientPackageVersion, LoadingCover
from . import feedback_signals as fb_signals

PackageVersion.sync_processor_class = PackageVersionProcessor

Advertisement.sync_processor_class = AdvertisementProcessor

Topic.sync_processor_class = TopicProcessor

Category.sync_processor_class = CategoryProcessor

ClientPackageVersion.sync_processor_class = ClientPackageVersionProcessor

LoadingCover.sync_processor_class = LoadingCoverProcessor


def feedback_start_action(sender, instance, operation, queue, **kwargs):
    pass


def pre_save_sync_files(sender, instance, **kwargs):
    if instance.pk is None:
        instance._sync_files = True
        return

    changed = instance.tracker.changed()
    for key, val in changed.items():
        if key in ('icon', 'cover', 'screenshots'):
            instance._sync_files = True
            return


def post_save_sync_files(sender, instance, **kwargs):
    try:
        if hasattr(instance, '_sync_files') and instance._sync_files:
            processor = instance.sync_processor_class(instance)
            processor.publish()
            del instance._sync_files
    except WorkingDirectoryNotFound:
        pass

#fb_signals.start_action.connect(feedback_start_action, sender=Feedback)

pre_save.connect(pre_save_sync_files, sender=PackageVersion)
pre_save.connect(pre_save_sync_files, sender=Advertisement)
pre_save.connect(pre_save_sync_files, sender=Category)
pre_save.connect(pre_save_sync_files, sender=Topic)
pre_save.connect(pre_save_sync_files, sender=ClientPackageVersion)
pre_save.connect(pre_save_sync_files, sender=LoadingCover)

post_save.connect(post_save_sync_files, sender=PackageVersion)
post_save.connect(post_save_sync_files, sender=Advertisement)
post_save.connect(post_save_sync_files, sender=Category)
post_save.connect(post_save_sync_files, sender=Topic)
post_save.connect(post_save_sync_files, sender=ClientPackageVersion)
post_save.connect(post_save_sync_files, sender=LoadingCover)

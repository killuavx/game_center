# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_save
from .core import Feedback
from .errors import WorkingDirectoryNotFound
from .processors.warehouse import PackageVersionProcessor
from .processors.taxonomy import TopicProcessor, CategoryProcessor
from .processors.promotion import AdvertisementProcessor
from warehouse.models import PackageVersion
from promotion.models import Advertisement
from taxonomy.models import Category, Topic
from . import feedback_signals as fb_signals

PackageVersion.sync_processor_class = PackageVersionProcessor

Advertisement.sync_processor_class = AdvertisementProcessor

Topic.sync_processor_class = TopicProcessor

Category.sync_processor_class = CategoryProcessor


def feedback_start_action(sender, instance, operation, queue, **kwargs):
    pass


def post_save_sync_files(sender, instance, **kwargs):
    created = kwargs.get('created', False)
    try:
        if created:
            processor = instance.sync_processor_class(instance)
            processor.publish()
    except WorkingDirectoryNotFound:
        pass

#fb_signals.start_action.connect(feedback_start_action, sender=Feedback)

"""
post_save.connect(post_save_sync_files, sender=PackageVersion)
post_save.connect(post_save_sync_files, sender=Advertisement)
post_save.connect(post_save_sync_files, sender=Category)
post_save.connect(post_save_sync_files, sender=Topic)
"""

# Create your models here.
from comment.models import Comment
from django.db.models.signals import post_save, post_delete
from mobapi2.utils import comment_list_cache_key_func
from django.core.cache import cache


def change_comment_updated_at(sender=None, instance=None, *args, **kwargs):
    data = dict(content_type=instance.content_type_id,
                object_pk=instance.object_pk)
    key = comment_list_cache_key_func.comment_updated_at.get_key(**data)
    cache.delete(key)


post_save.connect(receiver=change_comment_updated_at, sender=Comment)
post_delete.connect(receiver=change_comment_updated_at, sender=Comment)

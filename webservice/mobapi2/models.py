# Create your models here.
from django.utils.datastructures import SortedDict
from rest_framework.reverse import reverse as rest_reverse
from django.core.urlresolvers import reverse
from comment.models import Comment
from django.db.models.signals import post_save, post_delete
from mobapi2.rest_router import rest_router
from mobapi2.utils import comment_list_cache_key_func
from django.core.cache import cache
from django.utils.http import urlencode
import requests

PURGE_URL = "http://android.ccplay.com.cn/purge/?key=%s"

def api_comment_url(data, router=None):
    view_name = router.get_base_name('comment-list') if router else 'comment-list'
    url = rest_reverse(view_name)
    return "%s?%s" % (url, urlencode(data))


def web_comment_url(data):
    view_name = 'comment_list'
    url = reverse(view_name)
    return "%s?%s" % (url, urlencode(data))


def change_comment_updated_at(sender=None, instance=None, *args, **kwargs):
    data = dict(content_type=instance.content_type_id,
                object_pk=instance.object_pk)
    data = SortedDict(data)
    key = comment_list_cache_key_func.comment_updated_at.get_key(**data)
    cache.delete(key)

    api_url = api_comment_url(data, router=rest_router)
    web_url = web_comment_url(data)
    requests.head(PURGE_URL % api_url)
    requests.head(PURGE_URL % web_url)


post_save.connect(receiver=change_comment_updated_at, sender=Comment)
post_delete.connect(receiver=change_comment_updated_at, sender=Comment)

# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from comment.models import Comment

class CommentBaseDSL(object):

    _comment_url = '/api/comments/?content_type=%(ct)d&object_pk=%(op)d'

    @classmethod
    def setup(cls, context):
        pass

    @classmethod
    def teardown(cls, context):
        pass

    @classmethod
    def post(cls, context, obj, comment_content):
        ct = ContentType.objects.get_for_model(obj)
        api_url = cls._comment_url % dict(ct=ct.pk, op=obj.pk)
        context.client.post(api_url, dict(comment=comment_content))

    @classmethod
    def visit_comment_list(cls, context, obj):
        ct = ContentType.objects.get_for_model(obj)
        comment_url = cls._comment_url % dict(ct=ct.pk, op=obj.pk)
        context.client.get(comment_url)

    @classmethod
    def change_comment_publish_status(cls, context, the_comment, is_public):
        the_comment.is_public = is_public
        the_comment.save()

    @classmethod
    def get_comment_by(cls, obj):
        return Comment.objects.for_model(obj).get()



def factory_dsl(context):
    return CommentBaseDSL


def setup(context):
    factory_dsl(context).setup(context)


def teardown(context):
    factory_dsl(context).teardown(context)

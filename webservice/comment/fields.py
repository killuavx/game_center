# -*- coding: utf-8 -*-
from django.conf import settings
from mezzanine.generic.fields import CommentsField as MZCommentsField


class CommentsField(MZCommentsField):

    related_model = 'comment.Comment'

if "south" in settings.INSTALLED_APPS:
    try:
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules(rules=[((CommentsField,), [], {})],
                                patterns=["comment\.fields\."])
    except ImportError:
        pass

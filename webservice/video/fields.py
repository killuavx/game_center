# -*- coding: utf-8 -*-
from django.conf import settings
from toolkit.fields import FileWithMetaField


class VideoFileField(FileWithMetaField):

    pass


if "south" in settings.INSTALLED_APPS:
    try:
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules(rules=[
            ((FileWithMetaField,), [], {})
        ],
                                patterns=["video\.fields\."])
    except ImportError:
        pass

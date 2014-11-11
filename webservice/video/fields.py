# -*- coding: utf-8 -*-
from django.conf import settings
from toolkit.fields import FileWithMetaField
from django.db import models


class VideoFileField(FileWithMetaField):

    def _get_added_fields(self):
        fields = super(VideoFileField, self)._get_added_fields()
        fields['duration'] = ('%s_duration', models.FloatField(default=0,
                                                               blank=True,
                                                               editable=False))
        fields['width'] = ('%s_width', models.IntegerField(default=0,
                                                           blank=True,
                                                           editable=False))
        fields['height'] = ('%s_height', models.IntegerField(default=0,
                                                             blank=True,
                                                             editable=False))
        return fields

    def pre_save(self, model_instance, add):
        file = getattr(model_instance, self.attname)
        update_flag = False
        if file and not file._committed:
            update_flag = True

        if update_flag:
            mi = model_instance.media_info()
            setattr(model_instance,
                    self._field_name(self.attname, 'duration'),
                    mi.format.duration)

            video_stream = None
            for s in mi.streams:
                if s.type == 'video':
                    video_stream = s
                    break

            setattr(model_instance,
                    self._field_name(self.attname, 'height'),
                    video_stream.video_height)
            setattr(model_instance,
                    self._field_name(self.attname, 'width'),
                    video_stream.video_height)
        elif not file:
            setattr(model_instance,
                    self._field_name(self.attname, 'duration'),
                    0)
            setattr(model_instance,
                    self._field_name(self.attname, 'height'),
                    0)
            setattr(model_instance,
                    self._field_name(self.attname, 'width'),
                    0)
        return super(VideoFileField, self).pre_save(model_instance=model_instance,
                                                    add=add)


if "south" in settings.INSTALLED_APPS:
    try:
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules(rules=[
            ((FileWithMetaField,), [], {})
        ],
                                patterns=["video\.fields\."])
    except ImportError:
        pass

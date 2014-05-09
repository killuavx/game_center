# -*- coding: utf-8 -*-
import io
from django.conf import settings
from django.db.models import FloatField, IntegerField, FileField, CharField, BooleanField, TextField
from copy import deepcopy
from mezzanine.generic.fields import (
    BaseGenericRelation)
from django.core.files import File

import hashlib

def file_md5(f, iter_read_size=1024 ** 2 * 8):
    m = hashlib.md5()
    while True:
        data = f.read(iter_read_size)
        if not data:
            break
        m.update(data)
    return m.hexdigest()


def update_pkgfile_meta(instance, fieldname):
    from toolkit.fields import file_md5
    import io
    file_field = getattr(instance, fieldname)
    if file_field:
        with io.FileIO(file_field.path) as f:
            setattr(instance, '%s_md5' % fieldname, file_md5(f))
        setattr(instance, '%s_size' % fieldname, file_field.size)
        return instance
    return None


class StarsField(BaseGenericRelation):

    related_model = "toolkit.Star"
    fields = {"%s_count": IntegerField(default=0, editable=False),
              "%s_sum": IntegerField(default=0, editable=False),
              "%s_average": FloatField(default=0, editable=False),

              "%s_good_count": IntegerField(default=0, editable=False),
              "%s_good_rate": FloatField(default=0, editable=False),
              "%s_medium_count": IntegerField(default=0, editable=False),
              "%s_medium_rate": FloatField(default=0, editable=False),
              "%s_low_count": IntegerField(default=0, editable=False),
              "%s_low_rate": FloatField(default=0, editable=False),
    }

    def related_items_changed(self, instance, related_manager):
        """
        Calculates and saves the rating.
        """
        ratings = [r.value for r in related_manager.all()]
        instance = self._calc_base_value(instance, ratings)
        instance = self._calc_good_value(instance, ratings)
        instance = self._calc_medium_value(instance, ratings)
        instance = self._calc_low_value(instance, ratings)
        instance.save()

    def _calc_base_value(self, instance, ratings):
        count = len(ratings)
        _sum = sum(ratings)
        average = _sum / count if count > 0 else 0
        setattr(instance, "%s_count" % self.related_field_name, count)
        setattr(instance, "%s_sum" % self.related_field_name, _sum)
        setattr(instance, "%s_average" % self.related_field_name, average)
        return instance

    def _calc_good_value(self, instance, ratings):
        """
            good: star 4-5
                good_count = count(value in 4,5)
                good_rate = good_count / count(all)
        """
        _count, _rate = self.__calc_count_rate(instance, ratings, values=(4, 5))
        setattr(instance, "%s_good_count" % self.related_field_name, _count)
        setattr(instance, "%s_good_rate" % self.related_field_name, _rate)
        return instance

    def _calc_medium_value(self, instance, ratings):
        """
            medium: star 2-3
                medium_count = count(value in 2,3) / count(all)
                medium_rate = count(value in 2,3) / count(all)
        """
        _count, _rate = self.__calc_count_rate(instance, ratings, values=(2, 3))
        setattr(instance, "%s_medium_count" % self.related_field_name, _count)
        setattr(instance, "%s_medium_rate" % self.related_field_name, _rate)
        return instance

    def _calc_low_value(self, instance, ratings):
        """
            low: star 1
                low_count = count(value == 1)
                low_rate = low_count / count(all)
        """
        _count, _rate = self.__calc_count_rate(instance, ratings, values=(1,))
        setattr(instance, "%s_low_count" % self.related_field_name, _count)
        setattr(instance, "%s_low_rate" % self.related_field_name, _rate)
        return instance

    def __calc_count_rate(self, instance, ratings, values):
        vals_count = len(list(filter(lambda v: v in values, ratings)))
        all_count = getattr(instance, "%s_count" % self.related_field_name)
        rate = vals_count / all_count if all_count > 0 else 0
        return vals_count, rate


class FileWithMetaField(FileField):

    def __init__(self, *args, **kwargs):
        super(FileWithMetaField, self).__init__(*args, **kwargs)
        self.added_fields = self._get_added_fields()

    def _get_added_fields(self):
        return {
            "size": ('%s_size', IntegerField(default=0, editable=False)),
            "md5": ('%s_md5', CharField(default=None,
                                        null=True,
                                        blank=True,
                                        max_length=40,
                                        editable=False)),
        }

    def _field_name(self, attrname, name):
        return self.added_fields[name][0] % attrname

    def _field_type(self, name):
        return self.added_fields[name][1]

    def contribute_to_class(self, cls, name):
        if not cls._meta.abstract:
            for idx in self.added_fields.keys():
                cls.add_to_class(self._field_name(name, idx), self._field_type(idx))
        super(FileWithMetaField, self).contribute_to_class(cls, name)

    def pre_save(self, model_instance, add):
        file = getattr(model_instance, self.attname)
        update_flag = False
        if file and not file._committed:
            update_flag = True
        file = super(FileWithMetaField, self).pre_save(model_instance, add)

        if update_flag:
            _file_size = file.size
            with io.FileIO(file.path) as f:
                _md5_text = file_md5(f)
            setattr(model_instance, self._field_name(self.attname, 'size'), _file_size)
            setattr(model_instance, self._field_name(self.attname, 'md5'), _md5_text)
        elif not file:
            setattr(model_instance, self._field_name(self.attname, 'size'), 0)
            setattr(model_instance, self._field_name(self.attname, 'md5'), None)
        return file


class PkgFileField(FileWithMetaField):
    pass


# South requires custom fields to be given "rules".
# See http://south.aeracode.org/docs/customfields.html
if "south" in settings.INSTALLED_APPS:
    try:
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules(rules=[
            ((BaseGenericRelation,), [], {}),
            ((FileWithMetaField,), [], {})
        ],
                                patterns=["toolkit\.fields\."])
    except ImportError:
        pass

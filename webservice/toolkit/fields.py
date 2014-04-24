# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.models import FloatField, IntegerField
from mezzanine.generic.fields import (
    BaseGenericRelation)


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


# South requires custom fields to be given "rules".
# See http://south.aeracode.org/docs/customfields.html
if "south" in settings.INSTALLED_APPS:
    try:
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules(rules=[((BaseGenericRelation,), [], {})],
                                patterns=["toolkit\.fields\."])
    except ImportError:
        pass

# -*- coding: utf-8 -*-
import datetime
from django.utils.timezone import datetime, now, timedelta
from django_widgets import Widget
from taxonomy.models import Topic


class TopicsSummaryWidget(Widget):

    def get_context(self, value, options, context=None):
        cur_dt = now()
        current_month_count = Topic.objects\
            .published()\
            .filter(released_datetime__month=cur_dt.month()).count()
        total = Topic.objects.published().count()
        return options



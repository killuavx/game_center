# -*- coding: utf-8 -*-
import logging
from celery import app
from celery.utils.log import get_task_logger
from mongoengine import ValidationError
from analysis.documents.event import Event
from datetime import datetime
from dateutil import parser as dateparser
#logger = logging.getLogger('scripts')
logger = get_task_logger(__name__)


def event_fields_datetime_format_to_isostring(kwargs):
    created_datetime = kwargs.get('created_datetime')
    if created_datetime and isinstance(created_datetime, datetime):
        kwargs['created_datetime'] = created_datetime.isoformat()


def event_fields_datetime_format_to_datetime(kwargs):
    created_datetime = kwargs.get('created_datetime')
    if created_datetime:
        kwargs['created_datetime'] = dateparser.parse(created_datetime)





TASK_OK = 0

TASK_ABORT = 100

TASK_ABORT_OBJECT_NOT_EXIST = 101

TASK_ABORT_STATUS_NOT_PUBLISHED = 102

TASK_ABORT_OBJECT_NOT_MATCH = 103


@app.shared_task(name='analysis.tasks.record_event',
                 bind=True,
                 throws=(ValidationError, ),
                 max_retries=5,
                 default_retry_delay=60)
def record_event(self, **kwargs):
    event_fields_datetime_format_to_datetime(kwargs)
    try:
        Event(**kwargs).save()
    except ValidationError as e:
        raise
    except Exception as e:
        raise self.retry(exc=e, countdown=60)

    return TASK_OK

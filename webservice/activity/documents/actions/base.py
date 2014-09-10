# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.utils.timezone import now, get_default_timezone, is_aware, make_aware
from model_utils import Choices
from mongoengine import queryset, fields, errors
from mongoengine.document import DynamicDocument, EmbeddedDocument
from django.utils.translation import ugettext_lazy as _
from activity.documents.base import Ownerable
from account.documents.credit import CreditLog, CreditExchangable

PREFIX = 'activity'

db_alias = 'data_center'


def collection_name(name):
    return "%s_%s" %(PREFIX, name)


class TaskAlreadyDone(Exception):
    pass


class TaskConditionDoesNotMeet(Exception):
    pass


TASK_STATUS = Choices(
    ('posted', 'posted', _('Posted')),
    ('inprogress', 'inprogress', _('In Progress')),
    ('finish', 'finish', _('Just Finish')),
    ('done', 'done', _('Already Done')),
)


class Action(Ownerable, CreditExchangable, DynamicDocument):

    CODE = None

    name = fields.StringField()

    code = fields.StringField()

    created_datetime = fields.DateTimeField(default=lambda: now().astimezone())

    ip_address = fields.StringField(default='0.0.0.0')

    meta = {
        'allow_inheritance': True,
        'db_alias': db_alias,
        'collection': collection_name('action'),
        'indexes': [
            ('created_datetime', ),
            ('user_id', '-created_datetime', ),
        ],
        #'queryset_class':,
    }

    @property
    def content(self):
        raise NotImplementedError

    @content.getter
    def content(self, content):
        raise NotImplementedError

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.code = self.CODE
        return super(Action, self).save(*args, **kwargs)


class TaskRule(DynamicDocument):

    CODE = None

    name = fields.StringField()

    code = fields.StringField(unique=True)

    STATUS = TASK_STATUS

    def pre_update_action_check(self, task, action, *args, **kwargs):
        if task.id:
            return self.STATUS.inprogress
        else:
            return self.STATUS.posted

    def post_update_action_check(self, task, action, *args, **kwargs):
        if task.id:
            return self.STATUS.inprogress
        else:
            return self.STATUS.posted

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.code = self.CODE
        return super(TaskRule, self).save(*args, **kwargs)

    meta = {
        'allow_inheritance': True,
        'db_alias': db_alias,
        'collection': collection_name('taskrule'),
        'indexes': [],
    }


class TaskQuerySet(queryset.QuerySet):

    def with_user(self, user):
        return self.filter(user_id=user.pk)

    def in_date(self, action_datetime):
        begin_dt = datetime(year=action_datetime.year,
                            month=action_datetime.month,
                            day=action_datetime.day,
                            tzinfo=get_default_timezone())
        finish_dt = begin_dt + timedelta(days=1)
        return self.filter(created_datetime__gte=begin_dt,
                           created_datetime__lt=finish_dt)


class Task(Ownerable, CreditExchangable, DynamicDocument):

    CODE = None

    code = fields.StringField()

    rule = fields.ReferenceField(TaskRule, dbref=False)

    actions = fields.ListField(fields.ReferenceField(Action, dbref=False))

    created_datetime = fields.DateTimeField(default=lambda: now().astimezone())

    updated_datetime = fields.DateTimeField(default=lambda: now().astimezone())

    completed_datetime = fields.DateTimeField(required=False)

    ip_address = fields.StringField(default='0.0.0.0')

    STATUS = TASK_STATUS

    status = fields.StringField(choices=list(dict(STATUS).keys()), default=STATUS.posted)

    meta = {
        'allow_inheritance': True,
        'db_alias': db_alias,
        'collection': collection_name('task'),
        'indexes': [
            ('created_datetime', ),
            ('status', 'created_datetime', ),
            ('user_id', 'created_datetime', ),
            ('user_id', 'status', '-completed_datetime', ),
        ],
        'queryset_class': TaskQuerySet,
    }

    def process(self, user, action, rule, *args, **kwargs):
        rule_pre_check_status = rule.pre_update_action_check(task=self, action=action, *args, **kwargs)

        if TaskRule.STATUS.done == rule_pre_check_status:
            raise TaskAlreadyDone

        self.update_action(user=user, action=action,
                           rule=rule, rule_status=rule_pre_check_status,
                           *args, **kwargs)

        rule_status = rule.post_update_action_check(task=self, action=action, *args, **kwargs)

        if TaskRule.STATUS.done == rule_status:
            raise TaskAlreadyDone

        self.update_status(user=user, action=action, rule_status=rule_status, *args, **kwargs)

        self.save()

        if rule_status == TaskRule.STATUS.finish \
            and self.status == self.STATUS.done:
            self.make_done()

        return self

    def update_action(self, user, action, rule, rule_status, *args, **kwargs):
        if TaskRule.STATUS.posted == rule_status:
            self.user = user
            self.rule = rule
            self.credit_exchange_coin = getattr(self.rule, 'coin', 0)
            self.credit_exchange_experience = getattr(self.rule, 'experience', 0)

        if not action.id:
            action.save()

        self.actions.append(action)
        self.ip_address = action.ip_address
        self.updated_datetime = action.created_datetime

    def update_status(self, user, action, rule_status, *args, **kwargs):
        if rule_status == TaskRule.STATUS.finish:
            self.status = self.STATUS.done
        elif rule_status == TaskRule.STATUS.inprogress:
            self.status = self.STATUS.inprogress

        if self.status == self.STATUS.done:
            self.completed_datetime = self.updated_datetime

    def make_done(self):
        log = CreditLog.factory(exchangable=self,
                                user=self.user,
                                credit_datetime=self.completed_datetime)
        log.save()

    def save(self, *args, **kwargs):
        self.code = self.CODE
        return super(Task, self).save(*args, **kwargs)

    @classmethod
    def factory(cls, *args, **kwargs):
        """
            factory
                ::task
                ::user
                ::action
                ::rule
        """
        raise NotImplementedError

    @classmethod
    def factory_task(cls, user, action_datetime):
        try:
            qs = cls.objects.with_user(user).in_date(action_datetime).order_by('-created_datetime')
            task = qs[0]
        except IndexError:
            task = cls()
        return task

    @classmethod
    def get_rule_class(cls):
        raise NotImplementedError

    @classmethod
    def factory_rule(cls, *args, **kwargs):
        rule_cls = cls.get_rule_class()
        try:
            return rule_cls.objects.get(code=rule_cls.CODE)
        except:
            rule = rule_cls()
            rule.save()
            return rule

    @classmethod
    def get_action_class(cls):
        raise NotImplementedError

    @classmethod
    def factory_action(cls, *args, **kwargs):
        raise NotImplementedError

    @property
    def standard_count(self):
        raise NotImplementedError

    @property
    def progress(self):
        """
            progress::
                current, standard
        """
        return dict(
            current=len(self.actions),
            standard=self.standard_count
        )

    def __str__(self):
        dt = self.created_datetime.astimezone() \
            if is_aware(self.created_datetime) \
            else make_aware(self.created_datetime, get_default_timezone())
        return "%s, %s, %s" %(self.user,
                              dt.date(),
                              "%(current)d/%(standard)d" %self.progress)

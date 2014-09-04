# -*- coding: utf-8 -*-
from django.utils.timezone import now
from model_utils import Choices
from mongoengine import queryset, fields, errors
from mongoengine.document import DynamicDocument, EmbeddedDocument
from django.utils.translation import ugettext_lazy as _
from account.models import User

PREFIX = 'activity'

db_alias = 'data_center'


def collection_name(name):
    return "%s_%s" %(PREFIX, name)


class Ownerable(object):

    user_id = fields.IntField()

    @property
    def user(self):
        if not hasattr(self, '_user'):
            try:
                self._user = User.objects.get(pk=self.user_id)
            except:
                self._user = None
        return self._user

    @user.setter
    def user(self, user):
        self._user = user
        self.user_id = user.pk


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


class Action(Ownerable, DynamicDocument):

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


class Task(Ownerable, DynamicDocument):

    CODE = None

    rule = fields.ReferenceField(TaskRule, dbref=False)

    actions = fields.ListField(fields.ReferenceField(Action, dbref=False))

    created_datetime = fields.DateTimeField(default=lambda: now().astimezone())

    updated_datetime = fields.DateTimeField(default=lambda: now().astimezone())

    completed_datetime = fields.DateTimeField(required=False)

    STATUS = TASK_STATUS

    status = fields.StringField(choices=list(dict(STATUS).keys()), default=STATUS.posted)

    meta = {
        'allow_inheritance': True,
        'db_alias': db_alias,
        'collection': collection_name('task'),
        'indexes': [
            ('created_datetime', ),
            ('status', 'created_datetime', ),
            ('user_id', 'status', '-completed_datetime', ),
        ],
        #'queryset_class':,
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

        if not action.id:
            action.save()

        self.actions.append(action)
        self.updated_datetime = action.created_datetime

    def update_status(self, user, action, rule_status, *args, **kwargs):
        if rule_status == TaskRule.STATUS.finish:
            self.status = self.STATUS.done
        elif rule_status == TaskRule.STATUS.inprogress:
            self.status = self.STATUS.inprogress

        if self.status == self.STATUS.done:
            self.completed_datetime = self.updated_datetime

    def make_done(self):
        pass

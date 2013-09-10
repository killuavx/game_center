# -*- encoding=utf-8 -*-
from django.utils.translation import gettext_lazy as _
from functools import reduce


class AdminField(object):
    def __init__(self, name, method, admin_order_field=None, short_description=None, **kwargs):
        self.name = name
        self.method = method
        self.admin_order_field = admin_order_field
        self.field_path = name.split("__")
        self.short_description = short_description or _(self.field_path[-1])
        self.allow_tags = kwargs.get('allow_tags')
        self.boolean = kwargs.get('boolean')
        self.help_text = kwargs.get('help_text')

    def __call__(self, obj):
        return self.__dict__['method'](reduce(getattr, self.field_path, obj))

class AdminFieldBase(AdminField):
    DEFAULT_FIELD = None

    def __init__(self, name=None, *args, **kwargs):
        name = name or self.DEFAULT_FIELD
        super(AdminFieldBase, self).__init__(name, self.method, *args, **kwargs)

    @staticmethod
    def method(obj):
        raise NotImplemented


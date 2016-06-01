# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.reverse import reverse as rest_reverse

__author__ = 'me'


class PackageVersionHyperlinkedField(serializers.HyperlinkedRelatedField):

    def get_url(self, obj, view_name, request, format):
        kwargs = {'pk': obj.package.pk, 'vcode': obj.version_code}
        return rest_reverse(view_name, kwargs=kwargs, request=request, format=format)

    def get_object(self, queryset, view_name, view_args, view_kwargs):
        package_pk = view_kwargs['pk']
        version_code = view_kwargs['vcode']
        return queryset.get(package=package_pk, version_code=version_code)
# -*- coding: utf-8 -*-
from functools import wraps
import warnings
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.decorators import link
from rest_framework_extensions.mixins import DetailSerializerMixin
from activity.models import GiftBag, GiftCard
from mobapi2.authentications import PlayerTokenAuthentication
from mobapi2.activity.serializers import GiftBagSummarySerializer, GiftBagDetailSerializer, GiftCardSerializer
from mobapi2 import cache_keyconstructors as ckc
from rest_framework_extensions.cache.decorators import CacheResponse
from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import KeyConstructor
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework.decorators import permission_classes as rf_permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django.utils.decorators import method_decorator, available_attrs
from django.views.decorators.cache import never_cache
import json
from django.utils.timezone import now


class DataKeyConstructor(KeyConstructor):
    unique_method_id = bits.UniqueMethodIdKeyBit()
    format = bits.FormatKeyBit()
    language = bits.LanguageKeyBit()


class DataListKeyConstructor(DataKeyConstructor):
    list_sql_query = bits.ListSqlQueryKeyBit()
    pagination = bits.PaginationKeyBit()


class DataObjectKeyConstructor(DataKeyConstructor):
    retrieve_sql_query = bits.RetrieveSqlQueryKeyBit()


class CacheSerializerData(CacheResponse):

    def __call__(self, func):
        this = self
        @wraps(func, assigned=available_attrs(func))
        def inner(self, request, *args, **kwargs):
            return this.process_cache_serializerdata(
                view_instance=self,
                view_method=func,
                request=request,
                args=args,
                kwargs=kwargs,
                )
        return inner


    def process_cache_serializerdata(self,
                               view_instance,
                               view_method,
                               request,
                               args,
                               kwargs):
        key = self.calculate_key(
            view_instance=view_instance,
            view_method=view_method,
            request=request,
            args=args,
            kwargs=kwargs
        )
        data = self.cache.get(key)
        if not data:
            data = view_method(view_instance, request, *args, **kwargs)
            self.cache.set(key, json.dumps(data), self.timeout)
        else:
            data = json.loads(data)
        return data


cache_serializerdata = CacheSerializerData

import django_filters
from rest_framework.filters import DjangoFilterBackend


class GiftBagForPackageFilter(django_filters.FilterSet):

    for_package = django_filters.CharFilter(name='for_package_id')

    for_version = django_filters.CharFilter(name='for_version_id')

    class Meta:
        model = GiftBag
        fields = ('for_package', 'for_version', )


class GiftBagViewSet(DetailSerializerMixin,
                     viewsets.ReadOnlyModelViewSet):

    model = GiftBag
    serializer_class = GiftBagSummarySerializer
    serializer_detail_class = GiftBagDetailSerializer
    authentication_classes = (PlayerTokenAuthentication,)
    permission_classes = ()

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filter_class = GiftBagForPackageFilter
    ordering = ('-publish_date', )

    def get_queryset(self, is_for_detail=False):
        if self.queryset is None:
            self.queryset = self.model.objects.published()
        if self.queryset_detail is None:
            self.queryset_detail = self.model.objects.status_published()
        return super(GiftBagViewSet, self).get_queryset(is_for_detail=is_for_detail)

    cache_data_list_key_func = ckc.update_at_key_constructor(DataListKeyConstructor,
                                                             content_type='giftbag:cache',
                                                             hourly=True)()

    def list(self, request, *args, **kwargs):
        data = self._list_serializerdata(request, *args, **kwargs)
        now_timestamp = int(now().astimezone().strftime('%s'))
        for giftbag in data['results']:
            self.check_giftcard_status(giftbag, request.user, now_timestamp)
        return Response(data)


    @cache_serializerdata(key_func=cache_data_list_key_func)
    def _list_serializerdata(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())

        # Default is to allow empty querysets.  This can be altered by setting
        # `.allow_empty = False`, to raise 404 errors on empty querysets.
        if not self.allow_empty and not self.object_list:
            warnings.warn(
                'The `allow_empty` parameter is due to be deprecated. '
                'To use `allow_empty=False` style behavior, You should override '
                '`get_queryset()` and explicitly raise a 404 on empty querysets.',
                PendingDeprecationWarning
            )
            class_name = self.__class__.__name__
            error_msg = self.empty_error % {'class_name': class_name}
            raise Http404(error_msg)

        # Switch between paginated or standard style responses
        page = self.paginate_queryset(self.object_list)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)

        return serializer.data


    cache_data_object_key_func = ckc.update_at_key_constructor(DataObjectKeyConstructor,
                                                               content_type='giftbag-detail:cache',
                                                               hourly=True,
                                                               update_at_keybit=ckc.LookupObjectUpdatedAtKeyBit)()

    def retrieve(self, request, *args, **kwargs):
        data = self._retrieve_serializerdata(request, *args, **kwargs)
        now_timestamp = int(now().astimezone().strftime('%s'))
        self.check_giftcard_status(data, request.user, now_timestamp)
        return Response(data)

    @cache_serializerdata(key_func=cache_data_object_key_func)
    def _retrieve_serializerdata(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(self.object)
        return serializer.data

    def check_giftcard_status(self, giftbag, user, now_timestamp):
        giftbag_id = giftbag['id']
        if user and user.is_authenticated():
            cards = list(GiftCard.objects.took_from(giftbag_id).took_by(user))
            if cards:
                giftbag['has_took'] = True
                giftbag['code'] = cards[0].code
        giftbag['status'] = 'ok'

        if giftbag['expiry_datetime'] and int(giftbag['expiry_datetime']) <= now_timestamp:
            giftbag['status'] = 'expired'

        if int(giftbag['publish_datetime']) > now_timestamp:
            giftbag['status'] = 'unpublished'

        del giftbag['id']

    @method_decorator(rf_permission_classes((IsAuthenticated, )))
    @link()
    @method_decorator(never_cache)
    def take(self, request, *args, **kwargs):
        giftbag = self.get_object()
        cards = list(giftbag.get_took_cards_by(request.user))
        if cards:
            card = cards[0]
        else:
            card = giftbag.take_by(request.user)
        serializer = GiftCardSerializer(card)
        return Response(serializer.data)

    def get_permissions(self):
        _permission_classes = self.permission_classes
        handler = getattr(self, self.request.method.lower(), None)
        if handler and hasattr(handler, 'permission_classes'):
            _permission_classes = handler.permission_classes

        return [permission() for permission in _permission_classes]

# -*- coding: utf-8 -*-
from functools import wraps
import warnings
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.decorators import link, action
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
from rest_framework.filters import OrderingFilter, BaseFilterBackend
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


class GiftBagForOwnerFilterBackend(BaseFilterBackend):

    query_sql_exists = """SELECT id FROM %(gct)s
                          WHERE %(gct)s.giftbag_id=%(gbt)s.id
                          AND %(gct)s.owner_id=%(uid)s LIMIT 1"""

    def filter_queryset(self, request, queryset, view):
        if request.user and request.user.is_authenticated():
            sql_exists = self.query_sql_exists % dict(
                gct=GiftCard._meta.db_table,
                gbt=GiftBag._meta.db_table,
                uid=request.user.pk
            )
            return queryset.extra(where=['EXISTS( %s )' % sql_exists])
        else:
            return queryset.none()


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
                                                             hourly=False,
                                                             update_at_keybit=ckc.UserUpdatedAtKeyBit)()

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
                                                               hourly=False,
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
            self.cache_data_list_key_func.updated_at.pk = request.user.pk
            self.cache_data_list_key_func.updated_at.flush()
            self.cache_data_list_key_func.updated_at.pk = None

        serializer = GiftCardSerializer(card)
        return Response(serializer.data)

    def get_permissions(self):
        _permission_classes = self.permission_classes
        handler = getattr(self, self.request.method.lower(), None)
        if handler and hasattr(handler, 'permission_classes'):
            _permission_classes = handler.permission_classes

        return [permission() for permission in _permission_classes]

    @method_decorator(rf_permission_classes((IsAuthenticated,)))
    @method_decorator(never_cache)
    def mine(self, request, *args, **kwargs):
        orig_filter_backends, self.filter_backends =\
            self.filter_backends, [GiftBagForOwnerFilterBackend]+ list(self.filter_backends)

        self.kwargs.setdefault('user', True)
        data = self._list_serializerdata(request, *args, **kwargs)
        del self.kwargs['user']
        self.filter_backends = orig_filter_backends
        now_timestamp = int(now().astimezone().strftime('%s'))
        for giftbag in data['results']:
            self.check_giftcard_status(giftbag, request.user, now_timestamp)
        return Response(data)


from mobapi2.decorators import default_cache_control
from rest_framework_extensions.utils import (
    default_object_cache_key_func,
    default_list_cache_key_func,
    )
from activity.models import Note
from mobapi2.activity.serializers import NoteSummarySerializer, NoteDetailSerializer


class NoteViewSet(DetailSerializerMixin,
                  viewsets.ReadOnlyModelViewSet):

    lookup_field = 'slug'
    model = Note
    authentication_classes = ()
    permission_classes = ()
    serializer_class = NoteSummarySerializer
    serializer_detail_class = NoteDetailSerializer

    @cache_response(key_func=default_object_cache_key_func)
    @default_cache_control(max_age=3600*24*7)
    def retrieve(self, request, *args, **kwargs):
        return super(NoteViewSet, self).retrieve(request, *args, **kwargs)

    @cache_response(key_func=default_list_cache_key_func)
    @default_cache_control(max_age=3600*24*7)
    def list(self, request, *args, **kwargs):
        return super(NoteViewSet, self).list(request, *args, **kwargs)
        #return Response(status=status.HTTP_403_FORBIDDEN)



from activity.documents.scratchcard import ScratchCard, OwnerNotMatch
from activity.documents.scratchcard import generate_scratchcard_by_user, receive_scratchcard
from mobapi2.activity.serializers import WinnerScratchCardSerializer, GenerateScratchCardSerializer, AwardScratchCardSerializer
from mongoengine import DoesNotExist
from mobapi2.helpers import get_note_url


class ScratchCardViewSet(viewsets.GenericViewSet):

    base_name = 'scratchcard'

    note_slug = 'scratchcard'

    model = ScratchCard
    permission_classes = (IsAuthenticated, )
    authentication_classes = (PlayerTokenAuthentication,)

    SERIALIZER_CLS_WINNER = 'winner'
    SERIALIZER_CLS_GENERATE = 'generate'
    SERIALIZER_CLS_AWARD = 'award'
    serializer_classes = {
        SERIALIZER_CLS_GENERATE: GenerateScratchCardSerializer,
        SERIALIZER_CLS_WINNER: WinnerScratchCardSerializer,
        SERIALIZER_CLS_AWARD: AwardScratchCardSerializer,

    }
    serializer_class = AwardScratchCardSerializer

    def get_queryset(self):
        if not self.queryset:
            self.queryset = ScratchCard.objects.all()
        return self.queryset

    def get_serializer(self, instance=None, data=None,
                       files=None, many=False, partial=False,
                       cls_type=SERIALIZER_CLS_WINNER):
        serializer_class = self.get_serializer_class(cls_type)
        context = self.get_serializer_context()
        return serializer_class(instance, data=data, files=files,
                                many=many, partial=partial, context=context)

    def get_serializer_class(self, cls_type=SERIALIZER_CLS_WINNER):
        return self.serializer_classes[cls_type]

    @link()
    def play(self, request, *args, **kwargs):
        card = generate_scratchcard_by_user(request.user)
        if card.award_coin:
            card.save()
        card_serializer = self.get_serializer(card, cls_type=self.SERIALIZER_CLS_GENERATE)
        winner_serializer = self.get_winner_serializer(self.get_winner_list(),
                                                       many=True)
        return Response(data=dict(
            note_url=get_note_url(self.note_slug,
                                  router=card_serializer.opts.router,
                                  request=request,
                                  format=card_serializer.context.get('format')),
            scratchcard=card_serializer.data,
            winners=winner_serializer.data
        ))

    max_winner_items = 5

    def get_winner_list(self):
        return self.get_queryset().received()[0:self.max_winner_items]

    def get_winner_serializer(self, instance, many=False):
        return self.get_serializer(instance=instance,
                                   many=many,
                                   cls_type=self.SERIALIZER_CLS_WINNER)

    @action()
    def award(self, request, *args, **kwargs):
        qs = self.get_queryset()
        signcode = request.POST.get('signcode')
        if not signcode:
            data = dict(detail='invalid code')
            Response(data, status=status.HTTP_400_BAD_REQUEST)
        try:
            card = receive_scratchcard(qs, signcode=signcode, user=request.user)
            data = self.get_serializer(card, cls_type=self.SERIALIZER_CLS_AWARD).data
            status_code = status.HTTP_200_OK
        except DoesNotExist:
            data = dict(detail='invalid code')
            status_code = status.HTTP_400_BAD_REQUEST
        except OwnerNotMatch:
            data = dict(detail='invalid code')
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=status_code)


from mobapi2.activity.serializers import MyTasksStatusSerializer, TaskStatusSerializer
from activity.documents.actions.base import TaskAlreadyDone, TaskConditionDoesNotMeet
from activity.documents.actions.install import InstallTask
from activity.documents.actions.share import ShareTask
from warehouse.models import Package, PackageVersion
from toolkit.helpers import get_global_site


class TaskViewSet(viewsets.GenericViewSet):
    """ 任务接口

    ## 获取任务信息

        GET /api/v2/tasks/mystatus/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    ## 响应数据

        {
            // 评论
            "comment": {
                "experience": 10, //任务完成后奖励的成长经验
                "progress_current": 3, //当前进度
                "progress_standard": 3, //额定进度值
                "status": "done" //完成状态, done 已经完成
            },
            "install": {
                "experience": 10,
                "progress_current": 1,
                "progress_standard": 3,
                "status": "inprogress" //完成状态，进行中
            },
            "note_url": "http://a.ccplay.com.cn:8080/api/v2/notes/task/",
            "share": {
                "experience": 5,
                "progress_current": 0,
                "progress_standard": 5,
                "status": "posted" //完成状态，刚提交
            },
            "signin": {
                "experience": 10,
                "progress_current": 0,
                "progress_standard": 1,
                "status": "posted"
            },
            "summary": "\u4eca\u5929\u4f60\u5df2\u6512\u523010\u7ecf\u9a8c, \u7ee7\u7eed\u52a0\u6cb9\u54e6~" //描述内容
        }


    ## 请求数据:

    * `HTTP Header`: Authorization: Token `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`,
    * 通过登陆接口 [/api/v2/accounts/signin/](/api/v2/accounts/signin/)，获得登陆`Token <Key>`

    ## 响应状态

    * 200 HTTP_200_OK
        * 返回用户任务状态,
    * 401 HTTP_401_UNAUTHORIZED
        * 未登陆
        * 无效的HTTP Header: Authorization

    """

    base_name = 'task'
    note_slug = 'task'

    permission_classes = (IsAuthenticated, )
    authentication_classes = (PlayerTokenAuthentication,)
    serializer_class = MyTasksStatusSerializer

    def mystatus(self, request, *args, **kwargs):
        serializer = self.serializer_class.factory(request.user)
        data = serializer.data
        data['note_url'] = get_note_url(self.note_slug,
                                        router=serializer.opts.router,
                                        request=request,
                                        format=serializer.context.get('format'),
                                        )
        return Response(data)

    def get_packageversion(self, package_name, version_name):
        package = Package.all_objects.get_cache_by_alias(
            site_id=get_global_site().pk,
            package_name=package_name)
        if not package:
            return None
        version = PackageVersion \
            .all_objects \
            .get_cache_by_alias(package_id=package.pk,
                                version_name=version_name)
        return version

    def get_permissions(self):
        _permission_classes = self.permission_classes
        handler = getattr(self, self.request.method.lower(), None)
        if handler and hasattr(handler, 'permission_classes'):
            _permission_classes = handler.permission_classes

        return [permission() for permission in _permission_classes]

    def install(self, request, *args, **kwargs):
        ip_address = request.get_client_ip()
        package_name = request.DATA.get('package_name')
        version_name = request.DATA.get('version_name')
        version = self.get_packageversion(package_name=package_name,
                                          version_name=version_name)
        if not version:
            return Response(status=status.HTTP_404_NOT_FOUND)

        task, user, action, rule = InstallTask.factory(user=request.user,
                                                       version=version,
                                                       ip_address=ip_address)
        try:
            task.process(user=request.user, action=action, rule=rule)
        except TaskConditionDoesNotMeet:
            pass
        except TaskAlreadyDone:
            pass

        serializer = TaskStatusSerializer(task, many=False)
        return Response(serializer.data)

    def share(self, request, *args, **kwargs):
        ip_address = request.get_client_ip()
        package_name = request.DATA.get('package_name')
        version_name = request.DATA.get('version_name')
        version = self.get_packageversion(package_name=package_name,
                                          version_name=version_name)
        if not version:
            return Response(status=status.HTTP_404_NOT_FOUND)

        task, user, action, rule = ShareTask.factory(user=request.user,
                                                     version=version,
                                                     ip_address=ip_address)
        try:
            task.process(user=request.user, action=action, rule=rule)
        except TaskConditionDoesNotMeet:
            pass
        except TaskAlreadyDone:
            pass

        serializer = TaskStatusSerializer(task, many=False)
        return Response(serializer.data)


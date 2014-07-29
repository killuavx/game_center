# -*- coding: utf-8 -*-
from activity.models import GiftBag, GiftCard
from django.core.urlresolvers import reverse
from toolkit.helpers import qurl_to
from rest_framework import serializers
from mobapi2.serializers import HyperlinkedModelSerializer, ModelSerializer
from mobapi2.helpers import PackageDetailApiUrlEncode, PackageVersionDetailApiUrlEncode
from mobapi2.settings import IMAGE_ICON_SIZE


def giftbag_icon(giftbag):
    try:
        if giftbag.for_version_id:
            version = giftbag.for_version
        else:
            version = giftbag.for_package.versions.latest_published()
        return version.icon[IMAGE_ICON_SIZE].url
    except Exception as e:
        return None


def get_take_url(self, obj):
    view_name = self.opts.router.get_base_name('giftbag-take')
    take_url = reverse(view_name, kwargs=dict(pk=obj.pk))
    try:
        request = self.context.get('request')
        return request.build_absolute_uri(take_url)
    except AttributeError:
        pass
    return take_url


class GiftBagSummarySerializer(HyperlinkedModelSerializer):

    icon = serializers.SerializerMethodField('get_giftbag_icon')

    package_name = serializers.SerializerMethodField('get_package_name')

    def get_package_name(self, obj):
        return obj.for_package.package_name

    package_title = serializers.SerializerMethodField('get_package_title')

    def get_package_title(self, obj):
        try:
            return obj.for_version.title
        except:
            return obj.for_package.title


    def get_giftbag_icon(self, obj):
        if not hasattr(obj, '_icon_url'):
            obj._icon_url = giftbag_icon(obj)
        return obj._icon_url

    publish_datetime = serializers.DateTimeField(source='publish_date')

    expiry_datetime = serializers.DateTimeField(source='expiry_date')

    total_count = serializers.IntegerField(source='cards_total_count')

    remaining_count = serializers.IntegerField(source='cards_remaining_count')

    take = serializers.SerializerMethodField('get_take_url')

    has_took = serializers.SerializerMethodField('get_has_took')

    def get_has_took(self, obj):
        return False

    code = serializers.SerializerMethodField('get_code')

    def get_code(self, obj):
        return None

    get_take_url = get_take_url

    package_url = serializers.SerializerMethodField('get_package_url')

    def get_package_url(self, obj):
        request = self.context.get('request')
        router = self.opts.router
        if obj.for_version_id:
            return PackageVersionDetailApiUrlEncode(obj.for_version_id,
                                                    request=request,
                                                    router=router).get_url()
        else:
            return PackageDetailApiUrlEncode(obj.for_package_id,
                                             request=request,
                                             router=router).get_url()

    class Meta:
        model = GiftBag
        fields = ('url',
                  'title',
                  'package_name',
                  'package_title',
                  'icon',
                  'summary',
                  'publish_datetime',
                  'expiry_datetime',
                  'total_count',
                  'remaining_count',
                  'take',
                  'package_url',
                  'id',
                  'code',
                  'has_took',
        )


class GiftBagDetailSerializer(HyperlinkedModelSerializer):


    package_title = serializers.SerializerMethodField('get_package_title')

    def get_package_title(self, obj):
        try:
            return obj.for_version.title
        except:
            return obj.for_package.title

    package_name = serializers.SerializerMethodField('get_package_name')

    def get_package_name(self, obj):
        return obj.for_package.package_name

    icon = serializers.SerializerMethodField('get_giftbag_icon')

    def get_giftbag_icon(self, obj):
        if not hasattr(obj, '_icon_url'):
            obj._icon_url = giftbag_icon(obj)
        return obj._icon_url

    publish_datetime = serializers.DateTimeField(source='publish_date')

    expiry_datetime = serializers.DateTimeField(source='expiry_date')

    total_count = serializers.IntegerField(source='cards_total_count')

    remaining_count = serializers.IntegerField(source='cards_remaining_count')

    take = serializers.SerializerMethodField('get_take_url')

    get_take_url = get_take_url

    package_url = serializers.SerializerMethodField('get_package_url')

    has_took = serializers.SerializerMethodField('get_has_took')

    def get_has_took(self, obj):
        return False

    code = serializers.SerializerMethodField('get_code')

    def get_code(self, obj):
        return None

    def get_package_url(self, obj):
        request = self.context.get('request')
        router = self.opts.router
        if obj.for_version_id:
            return PackageVersionDetailApiUrlEncode(obj.for_version_id,
                                                    request=request,
                                                    router=router).get_url()
        else:
            return PackageDetailApiUrlEncode(obj.for_package_id,
                                             request=request,
                                             router=router).get_url()

    related_url = serializers.SerializerMethodField('get_related_url')

    def get_related_url(self, obj):
        router = self.opts.router
        reverse_viewname = 'giftbag-list'
        if router:
            reverse_viewname = router.get_base_name(reverse_viewname)
        url = reverse(reverse_viewname)

        request = self.context.get('request')
        url = qurl_to(url, for_package=obj.for_package_id)
        if request:
            url = request.build_absolute_uri(url)
        return url

    class Meta:
        model = GiftBag
        fields = ('url',
                  'title',
                  'package_name',
                  'package_title',
                  'icon',
                  'summary',
                  'usage_description',
                  'issue_description',
                  'publish_datetime',
                  'expiry_datetime',
                  'total_count',
                  'remaining_count',
                  'take',
                  'package_url',
                  'related_url',
                  'code',
                  'id',
                  'has_took',
        )


class GiftCardSerializer(ModelSerializer):

    took_datetime = serializers.DateTimeField(source='took_date')

    class Meta:
        model = GiftCard
        fields = (
            'code',
            'took_datetime',
        )

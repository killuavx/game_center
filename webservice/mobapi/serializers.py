# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.utils.http import urlencode

from rest_framework import serializers
from django.core.urlresolvers import reverse
from comment.models import Comment

from mobapi.rest_fields import factory_imageurl_field
from mobapi.settings import IMAGE_ICON_SIZE, IMAGE_COVER_SIZE

from taxonomy.models import Category, Topic, TopicalItem
from mobapi.helpers import get_item_model_by_topic


def get_url_for_taxonomy(request, obj, related_items, reverse_viewname):
    if related_items.count() > 0:
        path = reverse(reverse_viewname, kwargs=dict(slug=obj.slug))
        if request:
            return request.build_absolute_uri(path)
        return path
    return None


class CategoryRelatedChildrenMixin(object):
    def get_children(self, obj):
        qs = obj.children.showed()
        try:
            return CategorySummarySerializer(
                instance=qs,
                many=True,
                context=self.context).data
        except:
            return list()


class CategorySummarySerializer(CategoryRelatedChildrenMixin,
                                serializers.HyperlinkedModelSerializer):
    PREFIX = 'category'

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    children = serializers.SerializerMethodField('get_children')

    packages_url = serializers.SerializerMethodField('get_items_url')

    def get_items_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    obj.packages,
                                    '%s-packages' % self.PREFIX)

    class Meta:
        model = Category
        fields = ('url',
                  'icon',
                  'name',
                  'slug',
                  'packages_url',
                  'parent',
                  'children',
        )


class CategoryDetailSerializer(serializers.HyperlinkedModelSerializer):
    PREFIX = 'category'

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    packages_url = serializers.SerializerMethodField('get_items_url')

    def get_items_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    obj.packages,
                                    '%s-packages' % self.PREFIX)

    class Meta:
        model = Category
        fields = ('url',
                  'icon',
                  'name',
                  'slug',
                  'packages_url',
        )


class TopicRelatedItemCountUrlAndChildrenUrlMixin(object):
    PREFIX = 'topic'

    item_model_class = None

    def get_items_queryset(self, obj):
        return TopicalItem.objects \
            .get_items_by_topic(obj, get_item_model_by_topic(obj))

    def get_items_count(self, obj):
        return self.get_items_queryset(obj).published().count()

    def get_items_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    self.get_items_queryset(obj),
                                    '%s-items' % self.PREFIX)

    def get_children_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    obj.children,
                                    '%s-children' % self.PREFIX)


class TopicDetailWithPackageSerializer(
    TopicRelatedItemCountUrlAndChildrenUrlMixin,
    serializers.HyperlinkedModelSerializer):
    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = factory_imageurl_field(IMAGE_COVER_SIZE)

    items_url = serializers.SerializerMethodField('get_items_url')

    items_count = serializers.SerializerMethodField('get_items_count')

    children_url = serializers.SerializerMethodField('get_children_url')

    class Meta:
        model = Topic
        fields = ('url',
                  'icon',
                  'cover',
                  'name',
                  'slug',
                  'summary',
                  'children_url',
                  'items_url',
                  'items_count',
                  'updated_datetime',
                  'released_datetime')


class TopicSummarySerializer(
    TopicRelatedItemCountUrlAndChildrenUrlMixin,
    serializers.HyperlinkedModelSerializer):
    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = factory_imageurl_field(IMAGE_COVER_SIZE)

    items_url = serializers.SerializerMethodField('get_items_url')

    items_count = serializers.SerializerMethodField('get_items_count')

    children_url = serializers.SerializerMethodField('get_children_url')

    class Meta:
        model = Topic
        fields = ('url',
                  'icon',
                  'cover',
                  'children_url',
                  'items_url',
                  'items_count',
                  'name',
                  'slug',
                  'updated_datetime',
                  'released_datetime')

#---------------------------------------------------------------------------
from searcher.models import TipsWord


class TipsWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipsWord
        fields = ( 'keyword',
                   'weight' )

#---------------------------------------------------------------------------
from promotion.models import Advertisement


class AdvertisementSerializer(serializers.HyperlinkedModelSerializer):
    content_url = serializers.SerializerMethodField('get_content_url')

    def get_content_url(self, obj):
        hlid = serializers.HyperlinkedIdentityField(source='content',
                                                    view_name='package-detail',
        )
        hlid.context = self.context
        return hlid.field_to_native(obj.content, 'content_url')

    content_type = serializers.SerializerMethodField('get_content_type')

    def get_content_type(self, obj):
        return str(obj.content_type).lower()

    cover = factory_imageurl_field(None)

    class Meta:
        model = Advertisement
        fields = ( 'title',
                   'cover',
                   'content_url',
                   'content_type',
        )

#---------------------------------------------------------------------------
from account.models import User as Player


class AccountRelatedProfileMixin(object):
    def get_profile_icon_url(self, obj):
        try:
            return obj.profile.icon.url
        except:
            pass
        return None

    def get_profile_email(self, obj):
        try:
            return obj.profile.email
        except:
            pass
        return None

    def get_profile_phone(self, obj):
        try:
            return obj.profile.phone
        except:
            pass
        return None

    def get_comment_count(self, obj):
        try:
            return Comment.objects.with_site().published().filter(
                user=obj).count()
        except:
            return 0

    def get_profile_bookmark_count(self, obj):
        try:
            return obj.profile.bookmarks.published().count()
        except:
            pass
        return 0


class AccountDetailSerializer(AccountRelatedProfileMixin,
                              serializers.ModelSerializer):
    email = serializers.SerializerMethodField('get_profile_email')
    phone = serializers.SerializerMethodField('get_profile_phone')
    icon = serializers.SerializerMethodField('get_profile_icon_url')

    comment_count = serializers.SerializerMethodField('get_comment_count')

    bookmark_count = serializers \
        .SerializerMethodField('get_profile_bookmark_count')

    class Meta:
        model = Player
        fields = (
            'username',
            'icon',
            'comment_count',
            'bookmark_count',
        )

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
class CommentSerializer(serializers.ModelSerializer):
    user_icon = serializers.SerializerMethodField('get_user_icon_url')

    def get_user_icon_url(self, obj):
        try:
            return obj.user.profile.icon['small'].url
        except:
            return None

    class Meta:
        model = Comment
        fields = (
            'user_name',
            'user_icon',
            'comment',
            'submit_date',
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment


#---------------------------------------------------------------------------
from clientapp.models import ClientPackageVersion


class ClientPackageVersionSerializer(serializers.ModelSerializer):
    download = serializers.SerializerMethodField('get_download_url')

    def get_download_url(self, obj):
        if obj.download:
            return obj.download.url
        return None

    class Meta:
        model = ClientPackageVersion
        fields = (
            'package_name',
            'version_code',
            'version_name',
            'download',
            'download_size',
            'summary',
            'whatsnew',
            'released_datetime',
        )


def get_packageversion_comment_queryset(version):
    version_cmt = Comment.objects.for_model(version)
    return version_cmt.filter(is_public=True, is_removed=False)


def get_packageversion_comments_url(version):
    ct = ContentType.objects.get_for_model(version)
    kwargs = dict(content_type=ct.pk, object_pk=version.pk)
    url = reverse('comment-list')
    return "%s?%s" % (url, urlencode(kwargs))
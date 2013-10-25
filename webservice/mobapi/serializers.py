# -*- coding: utf-8 -*-
from rest_framework import serializers
from warehouse.models import Package, Author, PackageVersionScreenshot, PackageVersion
from comment.models import Comment
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.utils.http import urlencode
from easy_thumbnails.exceptions import InvalidImageFormatError

IMAGE_ICON_SIZE = 'middle'
IMAGE_COVER_SIZE = 'small'

class ImageUrlField(serializers.ImageField):

    size_alias = 'middle'

    def to_native(self, obj):
        if not obj:
            return None
        try:
            return obj[self.size_alias].url
        except (ValueError, KeyError, InvalidImageFormatError):
            return None

    def from_native(self, data):
        pass


def factory_imageurl_field(size_alias='middle'):
    field = ImageUrlField()
    field.size_alias = size_alias
    return field


class FileUrlField(serializers.FileField):

    def to_native(self, obj):
        try:
            return obj.url
        except ValueError:
            return None

    def from_native(self, data):
        pass

class AuthorSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ('url', 'name')

class PackageVersionScreenshotSerializer(serializers.ModelSerializer):

    large = serializers.SerializerMethodField('get_large_url')
    preview = serializers.SerializerMethodField('get_preview_url')

    # TODO 截图的预览地址，以及后台上传时的尺寸处理，
    def get_preview_url(self, obj):
        try:
            return obj.image['middle'].url
        except:
            return ''

    # TODO 截图的大图地址，以及后台上传时的尺寸处理，
    def get_large_url(self, obj):
        try:
            return obj.image['large'].url
        except:
            return ''

    class Meta:
        model = PackageVersionScreenshot
        fields = ('large', 'preview', 'rotate')

def get_packageversion_download_url(version):
    try:
        return version.di_download.url
    except ValueError: pass
    try:
        return version.download.url
    except ValueError: pass

    return None

def get_packageversion_download_size(version):
    try:
        return version.di_download.size
    except ValueError: pass
    try:
        return version.download.size
    except ValueError: pass

    return None

def get_packageversion_comment_queryset(version):
    version_cmt = Comment.objects.for_model(version)
    return version_cmt.filter(is_public=True, is_removed=False)

def get_packageversion_comments_url(version):
    ct = ContentType.objects.get_for_model(version)
    kwargs = dict(content_type=ct.pk, object_pk=version.pk)
    url = reverse('comment-list')
    return "%s?%s" % (url, urlencode(kwargs))

class PackageRelatedLatestVersinoMixin(object):

    serializer_class_screenshot = PackageVersionScreenshotSerializer

    def get_latest_version_name(self, obj):
        try:
            return obj.versions.latest_published().version_name
        except:
            return ''

    def get_latest_version_code(self, obj):
        try:
            return obj.versions.latest_published().version_code
        except:
            return ''

    def get_latest_version_whatsnew(self, obj):
        try:
            return obj.versions.latest_published().whatsnew
        except:
            return ''

    def get_latest_version_cover_url(self, obj):
        try:
            return obj.versions.latest_published().cover[IMAGE_COVER_SIZE].url
        except:
            return None

    def get_latest_version_icon_url(self, obj):
        try:
            return obj.versions.latest_published().icon[IMAGE_ICON_SIZE].url
        except:
            return None

    def get_latest_version_screenshots(self, obj):
        try:
            latest_version = obj.versions.latest_published()
            screenshots_serializer = self.serializer_class_screenshot(
                latest_version.screenshots.all(),
                many=True)
            return screenshots_serializer.data
        except:
            return dict()

    def get_latest_version_download(self, obj):
        latest_version = obj.versions.latest_published()
        return get_packageversion_download_url(latest_version)

    def get_latest_version_download_count(self, obj):
        latest_version = obj.versions.latest_published()
        return latest_version.download_count

    def get_latest_version_download_size(self, obj):
        latest_version = obj.versions.latest_published()
        return get_packageversion_download_size(latest_version)

    def get_latest_version_comment_count(self, obj):
        latest_version = obj.versions.latest_published()
        return get_packageversion_comment_queryset(latest_version).count()

    def get_latest_version_comments_url(self, obj):
        latest_version = obj.versions.latest_published()
        url = get_packageversion_comments_url(latest_version)
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(url)
        except AttributeError:
            pass
        return url

class PackageRelatedVersionsMixin(object):

    def get_version_count(self, obj):
        return obj.versions.published().count()

class PackageRelatedCategoryMixin(object):

    def get_main_category_name(self, obj):
        try:
            return obj.main_category.name
        except AttributeError:
            return None

    def get_categories_names(self, obj):
        names = (cat.name for cat in obj.categories.all())
        return names

class PackageActionsMixin(object):

    def get_action_links(self, obj):
        mark_url = None
        try:
            request = self.context.get('request')
            mark_url = request.build_absolute_uri(
                reverse('bookmark-detail',kwargs=dict(pk=obj.pk) )
            )
        except AttributeError: pass
        return dict(
           mark=mark_url,
        )

class PackageSummarySerializer(PackageRelatedVersionsMixin,
                               PackageRelatedLatestVersinoMixin,
                               PackageRelatedCategoryMixin,
                               PackageActionsMixin,
                               serializers.HyperlinkedModelSerializer):

    icon = serializers.SerializerMethodField('get_latest_version_icon_url')
    cover = serializers.SerializerMethodField('get_latest_version_cover_url')
    category_name = serializers.SerializerMethodField('get_main_category_name')
    categories_names = serializers.SerializerMethodField('get_categories_names')
    version_count = serializers.SerializerMethodField('get_version_count')
    download_size = serializers.SerializerMethodField('get_latest_version_download_size')
    comments_url = serializers.SerializerMethodField('get_latest_version_comments_url')
    actions = serializers.SerializerMethodField('get_action_links')

    author = AuthorSummarySerializer()
    class Meta:
        model = Package
        fields = ('url',
                  'icon',
                  'cover',
                  'package_name',
                  'title',
                  'tags',
                  'category_name',
                  'categories_names',
                  'version_count',
                  'summary',
                  'author',
                  'download_size',
                  'download_count',
                  'comments_url',
                  'released_datetime',
                  'actions',
        )

class PackageVersionSerializer(serializers.ModelSerializer):

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = factory_imageurl_field(IMAGE_COVER_SIZE)

    download = serializers.SerializerMethodField('get_version_download_url')
    def get_version_download_url(self, obj):
        return get_packageversion_download_url(obj)

    download_size = serializers.SerializerMethodField('get_version_download_size')
    def get_version_download_size(self, obj):
        return get_packageversion_download_size(obj)

    screenshots = PackageVersionScreenshotSerializer(many=True)

    comment_count = serializers.SerializerMethodField('get_version_comment_count')
    def get_version_comment_count(self, obj):
        version_cmt = get_packageversion_comment_queryset(obj)
        return version_cmt.count()

    comments_url = serializers.SerializerMethodField('get_version_comments_url')
    def get_version_comments_url(self, obj):
        url = get_packageversion_comments_url(obj)
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(url)
        except AttributeError:
            pass
        return url

    class Meta:
        model = PackageVersion
        fields = ('icon',
                  'cover',
                  'version_code',
                  'version_name',
                  'screenshots',
                  'whatsnew',
                  'download',
                  'download_count',
                  'download_size',
                  'comments_url',
                  'comment_count',
        )

class PackageDetailSerializer(PackageRelatedLatestVersinoMixin,
                              PackageRelatedCategoryMixin,
                              PackageActionsMixin,
                              serializers.HyperlinkedModelSerializer):

    icon = serializers.SerializerMethodField('get_latest_version_icon_url')
    cover = serializers.SerializerMethodField('get_latest_version_cover_url')
    version_name = serializers.SerializerMethodField('get_latest_version_name')
    version_code = serializers.SerializerMethodField('get_latest_version_code')
    whatsnew = serializers.SerializerMethodField('get_latest_version_whatsnew')
    screenshots = serializers.SerializerMethodField('get_latest_version_screenshots')
    category_name = serializers.SerializerMethodField('get_main_category_name')
    categories_names = serializers.SerializerMethodField('get_categories_names')
    download = serializers.SerializerMethodField('get_latest_version_download')
    download_count = serializers.SerializerMethodField('get_latest_version_download_count')
    download_size = serializers.SerializerMethodField('get_latest_version_download_size')
    comment_count = serializers.SerializerMethodField('get_latest_version_comment_count')
    comments_url = serializers.SerializerMethodField('get_latest_version_comments_url')

    actions = serializers.SerializerMethodField('get_action_links')

    author = AuthorSummarySerializer()
    versions = PackageVersionSerializer(many=True)

    class Meta:
        model = Package
        fields = ('url',
                  'icon',
                  'cover',
                  'package_name',
                  'title',
                  'version_code',
                  'version_name',
                  'download',
                  'download_count',
                  'download_size',
                  'comment_count',
                  'comments_url',
                  'tags',
                  'category_name',
                  'categories_names',
                  'whatsnew',
                  'summary',
                  'description',
                  'author',
                  'released_datetime',
                  'screenshots',
                  'versions',
                  'actions',
        )

class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = factory_imageurl_field(IMAGE_COVER_SIZE)

    packages_url = serializers.SerializerMethodField('get_packages_url')
    def get_packages_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('author-packages', kwargs=dict(pk=obj.pk))
        )

    class Meta:
        model = Author
        fields = ('url', 'icon', 'cover', 'name', 'packages_url')

#---------------------------------------------------------------
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
        return self.get_items_queryset(obj).count()

    def get_items_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    self.get_items_queryset(obj),
                                    '%s-items' %self.PREFIX)

    def get_children_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    obj.children,
                                    '%s-children' %self.PREFIX)

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

    cover = factory_imageurl_field('small')

    class Meta:
        model = Advertisement
        fields =( 'title',
                  'cover',
                  'content_url',
                  'content_type',
        )

#---------------------------------------------------------------------------
from account.models import Player, Profile
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

class AccountDetailSerializer(AccountRelatedProfileMixin,
                              serializers.ModelSerializer):

    email = serializers.SerializerMethodField('get_profile_email')
    phone = serializers.SerializerMethodField('get_profile_phone')
    icon = serializers.SerializerMethodField('get_profile_icon_url')

    comment_count = serializers.SerializerMethodField('get_comment_count')

    def get_comment_count(self, obj):
        return Comment.objects.with_site().published().filter(user=obj).count()

    class Meta:
        model = Player
        fields = (
            'username',
            'email',
            'phone',
            'icon',
            'comment_count',
        )

#---------------------------------------------------------------------------
class PackageUpdateSummarySerializer(PackageSummarySerializer):

    version_code = serializers.SerializerMethodField('get_latest_version_code')
    version_name = serializers.SerializerMethodField('get_latest_version_name')
    download = serializers.SerializerMethodField('get_latest_version_download')
    download_size = serializers.\
        SerializerMethodField('get_latest_version_download_size')
    is_updatable = serializers.SerializerMethodField('get_is_updatable')

    def get_is_updatable(self, obj):
        if getattr(obj, 'update_info', None) \
            and obj.update_info.get('version_code') is None:
            return False
        return self.get_latest_version_code(obj) > obj.update_info.\
                                                        get('version_code')
    class Meta:
        model = Package
        fields = ('url',
                  'icon',
                  'package_name',
                  'title',
                  'download',
                  'download_size',
                  'version_code',
                  'version_name',
                  'released_datetime',
                  'actions',
                  'is_updatable',
        )

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

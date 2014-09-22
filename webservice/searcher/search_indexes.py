# -*- coding: utf-8 -*-
from haystack import indexes
from warehouse.models import Package
from toolkit.helpers import get_global_site_id, get_global_site, set_global_site_id, SITE_DISABLE, SITE_NOT_SET
from django.conf import settings
icon_sizes_alias = settings.THUMBNAIL_ALIASES_ICON.keys()
cover_sizes_alias = settings.THUMBNAIL_ALIASES_COVER.keys()
screenshot_sizes_alias = settings.THUMBNAIL_ALIASES_SCREENSHOT.keys()

CharField = indexes.CharField

RESOURCE_ALIASES = ('default', 'pc20', 'web', 'pc')


class PackageSearchIndex(indexes.SearchIndex,
                         indexes.Indexable):

    text = indexes.CharField(document=True,
                             use_template=False)

    _version_ = indexes.IntegerField()

    author_id = indexes.IntegerField(model_attr='author_id')
    author_name = CharField(model_attr='author__name')

    tags_text = CharField(weight=100)

    title = CharField(weight=90)

    package_name = indexes.CharField(model_attr='package_name', weight=20)

    released_datetime = indexes.DateTimeField()
    updated_datetime = indexes.DateTimeField()

    # ERROR:root:Error updating warehouse using package
    # TypeError: expected bytes, bytearray or buffer compatible object
    site = indexes.IntegerField(model_attr='site_id')
    platform = indexes.CharField(default='android')

    def get_model(self):
        return Package

    def index_queryset(self, using=None):
        set_global_site_id(SITE_DISABLE)
        qs = self.get_model()._default_manager.published()
        set_global_site_id(SITE_NOT_SET)
        return qs

    def prepare(self, obj):
        self.prepared_data = super(PackageSearchIndex, self).prepare(obj)

        try:
            set_global_site_id(obj.site_id)
            self._prepare_platform(self.prepared_data, obj)
            self._prepare_summary(self.prepared_data, obj)
            self._prepare_latest_version(self.prepared_data, obj)
            self._prepare_version_detail(self.prepared_data, obj)
            self._prepare_images(self.prepared_data, obj)
            self._prepare_images_from_resources(self.prepared_data, obj)
            self._prepare_download(self.prepared_data, obj)
            self._prepare_tags(self.prepared_data, obj)
            self._prepare_full_categories(self.prepared_data, obj)
            self._prepare_all_topics(self.prepared_data, obj)
        except:
            raise
        finally:
            set_global_site_id(SITE_NOT_SET)

        return self.prepared_data

    def _prepare_platform(self, prepare_data, obj):
        if obj.is_android:
            prepare_data['platform'] = obj.PLATFORM_ANDROID
        if obj.is_ios:
            prepare_data['platform'] = obj.PLATFORM_IOS

    root_category_id = indexes.IntegerField(default=0)
    root_category_slug = indexes.CharField(weight=10, default='')
    root_category_name = indexes.CharField(weight=10, default='')

    primary_category_id = indexes.IntegerField(default=0)
    primary_category_name = indexes.CharField(weight=10, default='')
    primary_category_slug = indexes.CharField(weight=10, default='')

    main_categories = indexes.MultiValueField()
    main_category_ids = indexes.MultiValueField()

    categories = indexes.MultiValueField(weight=10)
    category_ids = indexes.MultiValueField()
    category_slugs = indexes.MultiValueField(weight=10)

    def _prepare_full_categories(self, prepare_data, obj):
        try:
            prepare_data['primary_category_id'] = obj.main_category.pk
            prepare_data['primary_category_name'] = obj.main_category.name
            prepare_data['primary_category_slug'] = obj.main_category.slug
        except:
            pass
        try:
            prepare_data['root_category_id'] = obj.root_category.pk
            prepare_data['root_category_name'] = obj.root_category.name
            prepare_data['root_category_slug'] = obj.root_category.slug
        except:
            pass

        cat_pools = set()
        main_categories = []
        main_category_ids = []
        for cat in obj.main_categories:
            main_categories.append(cat.name)
            main_category_ids.append(cat.pk)
            cat_pools.update(cat.get_ancestors(ascending=True,
                                               include_self=True))

        prepare_data['main_categories'] = main_categories
        prepare_data['main_category_ids'] = main_category_ids

        category_slugs = list()
        category_ids = list()
        categories = list()
        for c in cat_pools:
            category_ids.append(c.pk)
            category_slugs.append(c.slug)
            categories.append(c.name)
        prepare_data['categories'] = categories
        prepare_data['category_ids'] = category_ids
        prepare_data['category_slugs'] = category_slugs

    topics = indexes.MultiValueField(weight=10)
    topic_slugs = indexes.MultiValueField(weight=10)
    topic_ids = indexes.MultiValueField()

    def _prepare_all_topics(self, prepare_data, obj):
        topics = list()
        topic_ids = list()
        topic_slugs = list()
        for ti in obj.topics.all():
            topics.append(ti.topic.name)
            topic_ids.append(ti.topic.pk)
            topic_slugs.append(ti.topic.slug)
            prepare_data['topic_%d_ordering_i' % ti.topic.pk] = ti.ordering
        prepare_data['topics'] = topics
        prepare_data['topic_ids'] = topic_ids
        prepare_data['topic_slugs'] = topic_slugs

    latest_version_id = indexes.IntegerField()
    version_id = indexes.IntegerField()
    version_name = indexes.CharField(weight=20, indexed=False)
    version_code = indexes.IntegerField(default=0)

    star = indexes.FloatField(default=0)
    stars_count = indexes.IntegerField(default=0)
    stars_good_count = indexes.IntegerField(default=0, indexed=False)
    stars_good_rate = indexes.FloatField(default=0, indexed=False)
    stars_medium_count = indexes.IntegerField(default=0, indexed=False)
    stars_medium_rate = indexes.FloatField(default=0, indexed=False)
    stars_low_count = indexes.IntegerField(default=0, indexed=False)
    stars_low_rate = indexes.FloatField(default=0, indexed=False)

    summary = indexes.CharField(weight=10, default='')
    description = indexes.CharField(indexed=False, default='')
    whatsnew = indexes.CharField(indexed=False, default='')

    has_award = indexes.BooleanField(indexed=True, default=False)
    award_coin = indexes.IntegerField(indexed=True, default=0)

    def _prepare_summary(self, prepare_data, obj):
        latest_version = self._latest_version(obj)
        prepare_data['title'] = latest_version.subtitle or obj.title
        prepare_data['title'] = prepare_data['title'].strip()
        prepare_data['summary'] = latest_version.summary or obj.summary
        prepare_data['summary'] = prepare_data['summary'].strip()
        prepare_data['description'] = latest_version.description or obj.description
        prepare_data['whatsnew'] = latest_version.whatsnew


    def _prepare_latest_version(self, prepare_data, obj):
        latest_version = self._latest_version(obj)
        prepare_data['version_id'] = prepare_data['latest_version_id'] = latest_version.pk
        prepare_data['version_name'] = latest_version.version_name
        prepare_data['version_code'] = latest_version.version_code

        prepare_data['star'] = latest_version.stars_average
        prepare_data['stars_count'] = latest_version.stars_count
        prepare_data['stars_good_count'] = latest_version.stars_good_count
        prepare_data['stars_good_rate'] = latest_version.stars_good_rate
        prepare_data['stars_medium_count'] = latest_version.stars_medium_count
        prepare_data['stars_medium_rate'] = latest_version.stars_medium_rate
        prepare_data['stars_low_count'] = latest_version.stars_low_count
        prepare_data['stars_low_rate'] = latest_version.stars_low_rate

        prepare_data['has_award'] = latest_version.has_award
        prepare_data['award_coin'] = latest_version.award_coin

        prepare_data['released_datetime'] = latest_version.released_datetime.astimezone()
        prepare_data['updated_datetime'] = latest_version.updated_datetime.astimezone()

        lang_codes = latest_version.supported_languages.values_list('code', flat=True)
        prepare_data['support_language_codes'] = list(lang_codes)

    is_download_apk = indexes.BooleanField(indexed=True, default=False)
    is_download_cpk = indexes.BooleanField(indexed=True, default=False)

    download_size = indexes.IntegerField(indexed=False, default=0)
    download_url = indexes.CharField(indexed=False, default='')
    static_download_url = indexes.CharField(indexed=False, default='')
    download_count = indexes.IntegerField(indexed=False, default=0)
    total_download_count = indexes.IntegerField(indexed=False, default=0)

    is_free = indexes.BooleanField(index_fieldname='is_free_b')
    formatted_price = indexes.CharField(indexed=False,
                                        index_fieldname='formatted_price_s',
                                        default='free')

    support_ipad = indexes.BooleanField(index_fieldname='support_ipad_b')
    support_iphone = indexes.BooleanField(index_fieldname='support_iphone_b')
    support_idevices = indexes.BooleanField(index_fieldname='support_idevices_b')
    support_device_types = indexes.MultiValueField(indexed=False)
    support_language_codes = indexes.MultiValueField(indexed=False)

    def _prepare_version_detail(self, prepare_data, obj):
        latest_version = self._latest_version(obj)
        if obj.is_ios:
            iversion = latest_version.as_ios
            prepare_data['is_free_b'] = iversion.is_free()
            prepare_data['formatted_price_s'] = iversion.formatted_price
            prepare_data['support_ipad_b'] = iversion.support_ipad
            prepare_data['support_ipad_b'] = iversion.support_iphone
            prepare_data['support_idevices_b'] = iversion.support_alldevices
            prepare_data['support_device_types'] = iversion.device_types

    def _prepare_download(self, prepare_data, obj):
        latest_version = self._latest_version(obj)
        dw_url = latest_version.get_download_url(entrytype=None)
        try:
            prepare_data['download_url'] = self._site_build_absolute_uri(obj.site_id, dw_url)
            prepare_data['static_download_url'] = latest_version.get_download_url(entrytype=None, is_dynamic=False)
            prepare_data['is_download_cpk'] = latest_version.is_download_cpk()
            prepare_data['is_download_apk'] = latest_version.is_download_apk()
        except:
            pass
        prepare_data['download_size'] = latest_version.get_download_size()
        prepare_data['download_count'] = latest_version.download_count
        prepare_data['total_download_count'] = obj.download_count

    def _site_build_absolute_uri(self, site_id, path):
        return "http://%s%s" % (get_global_site(site_id).domain, path)

    def _prepare_images(self, prepare_data, obj):
        latest_version = self._latest_version(obj)
        if latest_version.icon:
            self._fetch_image_field_urls(prepare_data, 'icon', latest_version.icon, icon_sizes_alias)

        if latest_version.cover:
            self._fetch_image_field_urls(prepare_data, 'cover', latest_version.cover, cover_sizes_alias)

    def _prepare_images_from_resources(self, prepare_data, obj):
        latest_version = self._latest_version(obj)
        resources = getattr(latest_version, 'resources')
        kinds = ('cover', 'icon')
        for kind in kinds:
            for alias in RESOURCE_ALIASES:
                try:
                    res = getattr(resources, kind)[alias]
                    prepare_data['%s_%s_url' %(kind, alias)] = res.file.url
                except:
                    pass

    def _prepare_tags(self, prepare_data, obj):
        latest_version = self._latest_version(obj)
        tags = list(set(latest_version.tags_text.split() + obj.tags_text.split()))
        prepare_data['tags_text'] = " ".join(tags)

    def _latest_version(self, obj):
        return obj.latest_version

    def _fetch_image_field_urls(self, images, prefix, field, sizes_alias):
        try:
            default_url = field.url
        except:
            default_url = ''
        images["%s_%s_url" %(prefix, 'default')] = default_url
        for sa in sizes_alias:
            key = "%s_%s" %(prefix, sa)
            key_url = "%s_url" % key
            try:
                images[key_url] = field[sa].url
            except:
                images[key_url] = default_url

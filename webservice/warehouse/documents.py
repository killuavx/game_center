# -*- coding: utf-8 -*-
from warehouse import models as wh
from mongoengine import fields, document, errors
from mongoengine.queryset import QuerySet
from mongoengine import register_connection
from django.conf import settings

con_key = 'data_center'
con_opts = settings.MOGOENGINE_CONNECTS[con_key]
register_connection(alias=con_key,
                    name=con_opts.get('name'),
                    host=con_opts.get('host'),
                    port=con_opts.get('port'))


class PlatformRelated(object):

    platform = fields.StringField()


class SiteRelated(object):

    site_id = fields.IntField()


class Taxonomy(document.DynamicEmbeddedDocument,
               SiteRelated):

    id = fields.IntField()

    slug = fields.StringField()

    name = fields.StringField()

    _cls = fields.StringField()

    ordering = fields.IntField(default=0)

    meta = {'allow_inheritance': True}

    def __str__(self):
        return self.name


class Category(Taxonomy):
    pass


class Topic(Taxonomy):
    pass


class Author(document.EmbeddedDocument, SiteRelated):

    id = fields.IntField()

    name = fields.StringField()

    def __str__(self):
        return self.name


class PackageQuerySet(QuerySet):

    def by_topic(self, topic, ordering=None):
        qs = self.filter(taxonomies___cls='Topic')
        if isinstance(topic, int):
            qs = qs.filter(taxonomies__id=topic)
        elif isinstance(topic, str):
            qs = qs.filter(taxonomies__slug=topic)
        elif hasattr(topic, 'pk'):
            qs = qs.fields(taxonomies__id=topic.pk)
        else:
            raise TypeError

        if ordering in ('-', '+'):
            qs = qs.aggregate('topics').order_by('%staxonomies.ordering' % ordering)
        return qs

    def by_category(self, cat):
        qs = self.filter(taxonomies___cls='Category')
        if isinstance(cat, int):
            return qs.filter(taxonomies__id=cat)
        elif isinstance(cat, str):
            return qs.filter(taxonomies__slug=cat)
        elif hasattr(cat, 'pk'):
            return qs.fields(taxonomies__id=cat.pk)
        else:
            raise TypeError


class Stars(document.EmbeddedDocument):

    count = fields.IntField(default=0)

    sum = fields.IntField(default=0)

    average = fields.FloatField(default=0)

    good_count = fields.IntField(default=0)

    good_rate = fields.FloatField(default=0)

    medium_count = fields.IntField(default=0)

    medium_rate = fields.FloatField(default=0)

    low_count = fields.FloatField(default=0)

    low_rate = fields.FloatField(default=0)


class Comment(document.EmbeddedDocument):

    id = fields.IntField()

    user_icon = fields.StringField()

    user_name = fields.StringField()

    comment = fields.StringField()

    star = fields.IntField(required=False)

    submit_date = fields.DateTimeField()


class PackageVersionScreenshot(document.EmbeddedDocument):

    kind = fields.StringField()

    images = fields.DictField()

    alt = fields.StringField(default='')

    rotate = fields.StringField()

    def __str__(self):
        return "%s:%s" %(self.kind, self.alt)


class PackageVersionMixin(object):

    icons = fields.DictField()

    covers = fields.DictField(required=False)

    version_name = fields.StringField()

    version_code = fields.IntField()

    whatsnew = fields.StringField()

    download_url = fields.URLField()

    download_size = fields.IntField()

    download_md5 = fields.StringField(max_length=40)

    download_count = fields.IntField(default=0)

    supported_features = fields.ListField(fields.StringField(), required=False)

    supported_languages = fields.ListField(fields.StringField(), required=False)

    supported_devices = fields.ListField(fields.StringField(), required=False)

    stars = fields.EmbeddedDocumentField(Stars)

    comments = fields.SortedListField(fields.EmbeddedDocumentField(Comment),
                                      required=False,
                                      ordering='submit_date',
                                      reverse=True)

    screenshots = fields.ListField(fields.EmbeddedDocumentField(PackageVersionScreenshot))


class Package(document.DynamicDocument,
              PackageVersionMixin,
              PlatformRelated,
              SiteRelated):

    id = fields.IntField(primary_key=True)

    package_name = fields.StringField()

    author = fields.EmbeddedDocumentField(Author)

    # Description
    title = fields.StringField()

    summary = fields.StringField()

    description = fields.StringField()

    # date time
    released_datetime = fields.DateTimeField()

    update_datetime = fields.DateTimeField()

    # taxonomy
    tags = fields.ListField(fields.StringField())

    taxonomies = fields.ListField(fields.EmbeddedDocumentField(Taxonomy))

    root_category = fields.EmbeddedDocumentField(Category)

    primary_category = fields.EmbeddedDocumentField(Category)

    main_categories = fields.ListField(fields.EmbeddedDocumentField(Category))

    total_download_count = fields.IntField(default=0)

    meta = {
        'db_alias': 'data_center',
        'collection': wh.Package._meta.db_table,
        'index_background': True,
        'indexes': [
            ('platform', 'package_name', ),
            ('platform', '-released_datetime', ),
            ('platform', '-total_download_count', ),
            ('platform', '-download_count', ),
            ('platform', 'tags', ),
            ('platform', 'taxonomies'),
            ('platform', 'taxonomies._cls', 'taxonomies.id', '-taxonomies.ordering'),
            ('platform', 'taxonomies._cls', 'taxonomies.id', '-released_datetime'),
            #('platform', 'taxonomies._cls', 'taxonomies.id', '-download_count'),
            ('platform', 'taxonomies._cls', 'taxonomies.slug', '-taxonomies.ordering'),
            ('platform', 'taxonomies._cls', 'taxonomies.slug', '-released_datetime'),
            #('platform', 'taxonomies._cls', 'taxonomies.slug', '-download_count'),

            ('site_id', 'package_name', ),
            ('site_id', '-released_datetime', ),
            ('site_id', '-total_download_count', ),
            ('site_id', '-download_count', ),
            ('site_id', 'tags', ),
            ('site_id', 'taxonomies'),
            ('site_id', 'taxonomies._cls', 'taxonomies.id', '-taxonomies.ordering'),
            ('site_id', 'taxonomies._cls', 'taxonomies.id', '-released_datetime'),
            #('site_id', 'taxonomies._cls', 'taxonomies.id', '-download_count'),
            ('site_id', 'taxonomies._cls', 'taxonomies.slug', '-taxonomies.ordering'),
            ('site_id', 'taxonomies._cls', 'taxonomies.slug', '-released_datetime'),
            #('site_id', 'taxonomies._cls', 'taxonomies.slug', '-download_count'),

            # 按平台/根分类查询
            ('platform', 'root_category.id', '-released_datetime'),
            ('platform', 'root_category.slug', '-released_datetime'),
            ('platform', 'root_category.id', '-download_count'),
            ('platform', 'root_category.slug', '-download_count'),
            ('platform', 'root_category.id', '-total_download_count'),
            ('platform', 'root_category.slug', '-total_download_count'),

            # 按域名/根分类查询
            ('site_id', 'root_category.id', '-released_datetime'),
            ('site_id', 'root_category.slug', '-released_datetime'),
            ('site_id', 'root_category.id', '-download_count'),
            ('site_id', 'root_category.slug', '-download_count'),
            ('site_id', 'root_category.id', '-total_download_count'),
            ('site_id', 'root_category.slug', '-total_download_count'),

            'id',
            'comments.id',
            ('taxonomies.id', 'taxonomies._cls', )
        ],
        'queryset_class': PackageQuerySet,
        'ordering': ['site_id', '-released_datetime']
    }

    def __str__(self):
        return self.title


from mezzanine.core.templatetags.mezzanine_tags import gravatar_url
from toolkit.helpers import get_global_site
from django.conf import settings
icon_sizes_alias = settings.THUMBNAIL_ALIASES_ICON.keys()
cover_sizes_alias = settings.THUMBNAIL_ALIASES_COVER.keys()
screenshot_sizes_alias = settings.THUMBNAIL_ALIASES_SCREENSHOT.keys()


def sync_image_field(doc_field, field, sizes_alias):
    for sa in sizes_alias:
        try:
            doc_field[sa] = field[sa].url
        except:
            pass


class SyncPackageDocumentHandler(object):

    doc = None

    site = None

    package = None

    version = None

    def all_sync(self, package_orm, version_orm):
        try:
            pkg = Package.objects.get(id=package_orm.pk)
        except errors.DoesNotExist:
            pkg = Package(id=package_orm.pk)

        self.doc = pkg
        self.package, self.version = package_orm, version_orm
        self.site = get_global_site(self.package.site_id)

        self.sync_platform()
        self.sync_summary()
        self.sync_images()
        self.sync_stars()
        self.sync_tags()
        self.sync_taxonomies()
        self.sync_download()
        self.sync_comments()
        self.sync_supporteds()
        self.doc.save()
        return self.doc

    def sync_author(self):
        self.doc.author = Author.objects\
            .get_or_create(id=self.package.author.pk,
                           defaults=dict(
                               name=self.package.author.name
                           ))

    def sync_platform(self):
        self.doc.site_id = self.package.site_id
        if self.package.is_android:
            self.doc.platform = self.package.PLATFORM_ANDROID
        if self.package.is_ios:
            self.doc.platform = self.package.PLATFORM_IOS

    def sync_summary(self):
        self.doc.package_name = self.package.package_name
        self.doc.version_name = self.version.version_name
        self.doc.version_code = self.version.version_code
        self.doc.title = self.version.subtitle or self.package.title
        self.doc.whatsnew = self.version.whatsnew
        self.doc.summary = self.version.summary or self.package.summary
        self.doc.description = self.version.description or self.package.description
        self.doc.released_datetime = self.version.released_datetime.astimezone()
        self.doc.updated_datetime = self.version.updated_datetime.astimezone()

    def sync_tags(self):
        tags = set(self.package.tags_text.split() + self.version.tags_text.split())
        self.doc.tags.clear()
        [self.doc.tags.append(t) for t in tags]

    def site_build_absolute_uri(self, path):
        return "http://%s%s" % (self.site.domain, path)

    def sync_download(self):
        dw = self.version.get_download()
        dw_url = self.version.get_download_url(entrytype=None)
        self.doc.download_url = self.site_build_absolute_uri(dw_url)
        self.doc.download_size = self.version.get_download_size()
        self.doc.download_md5 = self.version.download_md5 if dw is self.version.download else self.version.di_download_md5
        self.doc.download_count = self.version.download_count
        self.doc.total_download_count = self.package.download_count

    def sync_stars(self):
        orm = self.version
        self.doc.stars = Stars(count=orm.stars_count,
                             sum=orm.stars_sum,
                             average=orm.stars_average,
                             good_count=orm.stars_good_count,
                             good_rate=orm.stars_good_rate ,
                             medium_count=orm.stars_medium_count,
                             medium_rate=orm.stars_medium_rate,
                             low_count=orm.stars_low_count,
                             low_rate=orm.stars_low_rate)

    def sync_taxonomies(self):
        self.doc.taxonomies.clear()
        self.sync_categories()
        self.sync_topics()

    def sync_topics(self):
        for ti in self.package.topics.all():
            self.doc.taxonomies.append(Topic(id=ti.topic.pk,
                                             name=ti.topic.name,
                                             slug=ti.topic.slug,
                                             ordering=ti.ordering))

    def sync_categories(self):
        self.doc.main_categories.clear()
        self.doc.root_category = None
        self.doc.primary_category = None
        main_categories = self.package.main_categories

        if self.package.main_category:
            pcat = self.package.main_category
            self.doc.primary_category = Category(id=pcat.pk,
                                                 name=pcat.name,
                                                 slug=pcat.slug)

        if self.package.root_category:
            rcat = self.package.root_category
            self.doc.root_category = Category(id=rcat.pk,
                                              name=rcat.name,
                                              slug=rcat.slug)

        cat_pools = set()
        for cat in main_categories:
            self.doc.main_categories.append(Category(id=cat.pk,
                                                     name=cat.name,
                                                     slug=cat.slug))
            cat_pools.update(cat.get_ancestors(ascending=True,
                                               include_self=True))

        for c in cat_pools:
            self.doc.taxonomies.append(Category(id=c.pk,
                                                name=c.name,
                                                slug=c.slug))

    def sync_images(self):
        self.doc.icons = dict()
        sync_image_field(self.doc.icons, self.version.icon, icon_sizes_alias)
        self.doc.covers = dict()
        if self.version.cover:
            sync_image_field(self.doc.covers, self.version.cover, cover_sizes_alias)
        self.sync_screenshots(screenshot_sizes_alias)

    def sync_screenshots(self, sizes_alias):
        self.doc.screenshots.clear()
        for s in self.version.screenshots.all():
            pvs = PackageVersionScreenshot(
                kind=s.kind,
                alt=s.alt,
                rotate=s.rotate
            )
            sync_image_field(pvs.images, s.image, sizes_alias)
            self.doc.screenshots.append(pvs)

    def sync_comments(self):
        self.doc.comments.clear()
        comments = self.version.comments.all().visible()
        for cmt in comments:
            try:
                star = cmt.content_star.get().value
            except:
                star = None
            self.doc.comments.append(
                Comment(id=cmt.pk,
                        user_icon=gravatar_url(cmt.email),
                        user_name=cmt.user.username if cmt.user else None,
                        star=star,
                        comment=cmt.comment,
                        submit_date=cmt.submit_date.astimezone())
            )

    def sync_supporteds(self):
        self.doc.supported_languages = list(self.version.supported_languages\
            .values_list('code', flat=True))
        self.doc.supported_devices = list(self.version.supported_devices\
            .values_list('code', flat=True))
        self.doc.supported_features = list(self.version.supported_features\
            .values_list('code', flat=True))

    def delete(self, package_id):
        try:
            Package.objects.get(id=package_id).delete()
        except:
            pass


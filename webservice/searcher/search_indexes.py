# -*- coding: utf-8 -*-
from haystack import indexes
from warehouse.models import Package
from toolkit.managers import current_site_enable

CharField = indexes.CharField


class PackageSearchIndex(indexes.SearchIndex, indexes.Indexable):


    text = indexes.CharField(document=True,
                             use_template=False)

    _version_ = indexes.IntegerField()

    author_name = CharField(model_attr='author__name')

    tags_text = CharField(model_attr='tags_text',
                          weight=100)

    title = CharField(model_attr='title',
                      weight=90)

    package_name = indexes.CharField(model_attr='package_name',
                                     weight=20)

    categories = indexes.MultiValueField(weight=10)
    category_ids = indexes.MultiValueField(weight=10)
    category_slugs = indexes.MultiValueField(weight=10)

    released_datetime = indexes.DateTimeField(model_attr='released_datetime')

    updated_datetime = indexes.DateTimeField(model_attr='updated_datetime')

    # ERROR:root:Error updating warehouse using package
    # TypeError: expected bytes, bytearray or buffer compatible object
    site = indexes.IntegerField(model_attr='site_id')

    def get_model(self):
        return Package

    def index_queryset(self, using=None):
        qs = self.get_model()._default_manager.published()
        return qs

    def prepare(self, obj):
        prepare_data = super(PackageSearchIndex, self).prepare(obj)
        categories = obj.categories.all()
        prepare_data['category_slugs'] = [cat.slug for cat in categories]
        prepare_data['category_ids'] = [cat.pk for cat in categories]
        prepare_data['categories'] = [cat.name for cat in categories]
        return prepare_data


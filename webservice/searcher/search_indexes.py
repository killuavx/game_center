# -*- coding: utf-8 -*-
from haystack import indexes
from warehouse.models import Package

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

    categories = indexes.MultiValueField(model_attr='categories__all',
                                         weight=10)

    released_datetime = indexes.DateTimeField(model_attr='released_datetime')

    updated_datetime = indexes.DateTimeField(model_attr='updated_datetime')

    site = indexes.IntegerField(model_attr='site')

    def get_model(self):
        return Package

    def index_queryset(self, using=None):
        return self.get_model().objects.published()

    def prepare_categories(self, obj):
        return [category.name for category in obj.categories.published()]


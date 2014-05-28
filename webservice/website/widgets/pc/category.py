# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from .base import BaseComplexPackageListWidget, BaseWidgetFilterBackend
from website.widgets.common.package import BasePackageListWidget
from django_widgets import Widget
import six


__all__ = ['PCCategorySelectorWidget', 'PCCategoryComplexPackageList']


class PCCategorySelectorWidget(Widget):

    def get_category_selectlist(self, category):
        catlist = list(category.get_leafnodes())
        catlist.insert(0, category)
        return catlist

    def get_second_selectlist(self):
        from taxonomy.models import Topic
        from mezzanine.conf import settings
        slug_text = getattr(settings, 'GC_PC_COMPLEX_PACKAGE_FILTER_TOPIC_SLUGS')
        slugs = list(filter(lambda x: x, slug_text.split(',')))

        #slugs = slugs + ['ZH', 'EN']
        result = []
        for s in slugs:
            params = dict(topic=None, lang=None)
            if s == 'NONE':
                result.append(dict(params=params, name='最新发布'))
            elif s in ('ZH', 'EN'):
                params['lang'] = s
                if s == 'ZH':
                    result.append(dict(params=params, name='中文'))
                if s == 'EN':
                    result.append(dict(params=params, name='英文'))
            else:
                try:
                    topic = Topic.objects.get(slug=s)
                except ObjectDoesNotExist:
                    continue
                params['topic'] = topic.pk
                result.append(dict(params=params, name=topic.name))
        return result

    def get_context(self, value, options):
        root_category = options.get('root_category')
        category_selectlist = self.get_category_selectlist(root_category)
        second_selectlist = self.get_second_selectlist()
        return dict(
            category_selectlist=category_selectlist,
            second_selectlist=second_selectlist,
        )


class PCCategoryComplexPackageList(BasePackageListWidget, Widget):

    class ByLanguageFitlerBackend(BaseWidgetFilterBackend):

        def filter_queryset(self, request, queryset, widget):
            if widget.lang:
                return queryset.filter(versions__supported_languages=widget.lang.pk)
            return queryset

    ByCategoryFilterBackend = BaseComplexPackageListWidget.ByCategoryFilterBackend
    ByTopicFilterBackend = BaseComplexPackageListWidget.ByTopicFilterBackend
    OrderByFilterBackend = BaseComplexPackageListWidget.OrderByFilterBackend

    filter_backends = (
        ByCategoryFilterBackend,
        ByTopicFilterBackend,
        OrderByFilterBackend,
        #ByLanguageFitlerBackend,
    )

    ordering = ()

    current_topic = None

    category = None

    lang = None

    def get_category(self, slug):
        from taxonomy.models import Category
        if isinstance(slug, six.string_types):
            return Category.objects.get(slug=slug)
        elif isinstance(slug, Category):
            return slug
        raise TypeError

    def get_topic(self, slug):
        from taxonomy.models import Topic
        if not slug:
            return None
        if isinstance(slug, six.string_types):
            return Topic.objects.get(slug=slug)
        elif isinstance(slug, Topic):
            return slug
        raise TypeError

    def get_lang(self, lang):
        from warehouse.models import SupportedLanguage
        return SupportedLanguage.objects.get(code=lang)

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        self.category = self.get_category(options.get('category'))
        try:
            self.current_topic = self.get_topic(options.get('topic'))
        except ObjectDoesNotExist:
            self.current_topic = None

        try:
            self.lang = self.get_lang(options.get('lang'))
        except ObjectDoesNotExist:
            self.lang = None

        data = super(PCCategoryComplexPackageList, self).get_context(value=value,
                                                                     options=options,
                                                                     context=context,
                                                                     pagination=pagination)
        return data

# -*- coding: utf-8 -*-
from fts.helpers import add_model_objects, clear_data
from promotion.models import Place, Advertisement, Advertisement_Places
from django.contrib.contenttypes.models import ContentType
from should_dsl import should, should_not
from django.utils.timezone import now, timedelta


class PromotionBaseDSL(object):

    _adv_url = '/api/advertisements/'

    @classmethod
    def setup(cls, context):
        pass

    @classmethod
    def teardown(cls, context):
        clear_data()

    @classmethod
    def create_advertisements(cls,
                              context,
                              content_rows,
                              place_slug):
        rtn = []
        place = Place.objects.get(slug=place_slug)
        for row in content_rows:
            _kwargs = cls._get_adv_kwargs(**row)
            adv = cls.create_adv(ordering=row.get('ordering'),
                                 place=place,
                                 **_kwargs)
            rtn.append(adv)
        return rtn

    @classmethod
    def _get_adv_kwargs(cls, **kwargs):
        yesterday = now() - timedelta(days=1)
        content_type = kwargs.pop('content_type')
        content_type |should_not| be(None)
        ct = ContentType.objects.get(model=content_type)
        object_field = kwargs.pop('object_field')
        object_value = kwargs.pop('object_value')
        obj = ct.get_object_for_this_type(**{
            object_field: object_value
        })
        _kwargs = dict()
        _kwargs.update(
            title=kwargs.get('title'),
            status=kwargs.get('status', 'published'),
            content=obj,
            released_datetime=kwargs.get('released_datetime', yesterday)
        )

        return _kwargs


    @classmethod
    def create_adv(cls, place=None, ordering=None, **kwargs):
        adv = Advertisement.objects.create(**kwargs)
        ap = Advertisement_Places.objects.create(place=place, advertisement=adv)
        if ordering is not None:
            ap.ordering = ordering
            ap.save()
        add_model_objects(adv)
        add_model_objects(ap)
        return adv

    @classmethod
    def create_place(cls, context, slug):
        place = Place.objects.create(slug=slug)
        add_model_objects(place)
        return place

    @classmethod
    def visit_advertisements_page(cls, context, place_slug=None):
        api_url = cls._adv_url
        if place_slug:
            api_url = "%s?place=%s" % (cls._adv_url, place_slug)
        return context.browser.visit(api_url)


def factory_dsl(context):
    return PromotionBaseDSL


def setup(context):
    return factory_dsl(context).setup(context)


def teardown(context):
    return factory_dsl(context).teardown(context)

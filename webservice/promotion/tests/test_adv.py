"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from datetime import timedelta
from django.test import TestCase
from django.utils.timezone import now
from promotion.models import Advertisement, Place
from fts.tests.helpers import ApiDSL


class PlaceUnitTest(TestCase):

    def test_basic_create(self):
        place = Place(slug='mobile-home-top', help_text='手机端的首页顶部')
        place.save()

        except_place = Place.objects.get(pk=place.pk)
        self.assertEqual(except_place.slug, 'mobile-home-top')

class AdvUnitTest(TestCase):

    def create_place(self, **default):
        return Place.objects.create(**default)

    def test_basic_create_adverisement(self):
        pkg = ApiDSL.Given_i_have_published_package(self,
                                                        title='愤怒的小鸟：星球大战')
        adv = Advertisement(title='愤怒的小鸟 愤怒地登场', content=pkg)
        adv.save()
        self.assertEqual(adv.title, '愤怒的小鸟 愤怒地登场')
        self.assertEqual(adv.status, adv.STATUS.draft)
        self.assertEqual(adv.content.title, '愤怒的小鸟：星球大战')

        self.assertEqual(adv.is_published(), False)

    def test_adverisement_place_to_show(self):
        yestoday = now()-timedelta(days=1)
        pkg = ApiDSL.Given_i_have_published_package(self,
                                                    title='愤怒的小鸟：星球大战')
        adv = Advertisement.objects.create(title='愤怒的小鸟 愤怒地登场',
                            content=pkg,
                            released_datetime=yestoday,
                            status=Advertisement.STATUS.published
                            )
        p1 = self.create_place(slug='mobile-home-top')
        adv.places.add(p1)
        p2 = self.create_place(slug='website-home-top')
        adv.places.add(p2)
        self.assertEqual(2, adv.places.count())
        self.assertEqual(adv.is_published(), True)

# -*- encoding: utf-8-*-
from fts import helpers
from fts.helpers import RestApiTest, ApiDSL
from promotion.models import Place, Advertisement, Advertisement_Places
from django.utils.timezone import now, timedelta
from rest_framework import status

class AdvertisementRestApiTest(RestApiTest):

    def Given_i_have_place(self, **default):
        return Place.objects.create(**default)

    def Given_i_have_advertisement_with(self, **default):
        adv = Advertisement(**default)
        adv.save()
        return adv

    def _add_relationship(self, adv, place):
        Advertisement_Places.objects.create( advertisement=adv,
                                             place=place)

    def test_advertisement_list_without_place_should_receive_error(self):
        """没有place的情况下，广告是没有作用的"""
        yestoday = now()-timedelta(days=1)
        place = self.Given_i_have_place(slug='mobile-home-top')
        pkg = ApiDSL.Given_i_have_published_package(self)
        adv = self.Given_i_have_advertisement_with(content=pkg,
                                             title='疯狂地赛车',
                                             status=Advertisement.STATUS.published,
                                             released_datetime=yestoday
                                             )
        ApiDSL.When_i_access_advertisement_with(self, place=None)
        ApiDSL.Then_i_should_receive_response_with(self,
                                       status_code=status.HTTP_403_FORBIDDEN)

    def test_should_receive_advertisement_list_with_place(self):
        """ 同一个place下的广告列表，一个广告列表展示 """
        yestoday = now()-timedelta(days=1)
        place = self.Given_i_have_place(slug='mobile-home-top')
        pkg = ApiDSL.Given_i_have_published_package(self)
        adv = self.Given_i_have_advertisement_with(
                                             content=pkg,
                                             title='疯狂地赛车',
                                             status=Advertisement.STATUS.published,
                                             released_datetime=yestoday
        )
        self._add_relationship(adv, place)
        ApiDSL.When_i_access_advertisement_with(self, place=place)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_result_list(self, num=1)

        results = self.world.get('content').get('results')
        ApiDSL.Then_i_should_see_advertisement_list(self, adv_list=results)

    def test_should_receive_same_place_advertisement_list_by_ordering(self):
        """ 同一个place下的广告列表，按ordering顺序排序展示 """
        yestoday = now()-timedelta(days=1)
        place = self.Given_i_have_place(slug='mobile-home-top')
        pkg = ApiDSL.Given_i_have_published_package(self)
        adv1 = self.Given_i_have_advertisement_with(
                                            content=pkg,
                                            title='疯狂地赛车',
                                            status=Advertisement.STATUS.published,
                                            released_datetime=yestoday
        )
        self._add_relationship(adv1, place)

        pkg2 = ApiDSL.Given_i_have_published_package(self)
        adv2 = self.Given_i_have_advertisement_with(
                                             content=pkg2,
                                             title='我叫MT',
                                             status=Advertisement.STATUS.published,
                                             released_datetime=yestoday
        )
        self._add_relationship(adv2, place)

        # reverse
        relation2 = Advertisement.places.through\
                            .objects.filter(advertisement=adv2, place=place)\
                            .get()
        relation2.ordering = 0
        relation2.save()

        relation1 = Advertisement.places.through \
            .objects.filter(advertisement=adv1, place=place) \
            .get()
        relation1.ordering = 1
        relation1.save()

        ApiDSL.When_i_access_advertisement_with(self, place=place)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_result_list(self, num=2)

        results = self.world.get('content').get('results')
        ApiDSL.Then_i_should_see_advertisement_list(self, adv_list=results)

        except_adv2 = results[0]
        except_adv1 = results[1]
        self.assertEqual(except_adv1.get('title'), adv1.title)
        self.assertEqual(except_adv2.get('title'), adv2.title)

    def test_should_receive_advertisement_list_within_diff_place_by_ordering(self):
        """ 两个广告位，两个广告,分别对应关系 mobile-home-top(adv1, adv2), website-home-top(adv1)
            分别访问不同广告位，返回对应的广告列表
        """
        yestoday = now()-timedelta(days=1)
        mobile_place = self.Given_i_have_place(slug='mobile-home-top')
        website_place = self.Given_i_have_place(slug='website-home-top')
        pkg = ApiDSL.Given_i_have_published_package(self)
        adv1 = self.Given_i_have_advertisement_with(
                                                    content=pkg,
                                                    title='疯狂地赛车',
                                                    status=Advertisement.STATUS.published,
                                                    released_datetime=yestoday
        )
        self._add_relationship(adv1, mobile_place)
        self._add_relationship(adv1, website_place)

        pkg2 = ApiDSL.Given_i_have_published_package(self)
        adv2 = self.Given_i_have_advertisement_with(content=pkg2,
                                                    title='我叫MT',
                                                    status=Advertisement.STATUS.published,
                                                    released_datetime=yestoday
        )
        self._add_relationship(adv2, mobile_place)

        # reverse mobile_place
        relation2 = Advertisement.places.through \
            .objects.filter(advertisement=adv2, place=mobile_place) \
            .get()
        relation2.ordering = 0
        relation2.save()

        relation1 = Advertisement.places.through \
            .objects.filter(advertisement=adv1, place=mobile_place) \
            .get()
        relation1.ordering = 1
        relation1.save()

        ApiDSL.When_i_access_advertisement_with(self, place=mobile_place)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_result_list(self, num=2)

        results = self.world.get('content').get('results')
        ApiDSL.Then_i_should_see_advertisement_list(self, adv_list=results)


        self.assertListEqual(
            [results[0].get('title'), results[1].get('title')],
            [adv2.title, adv1.title]
        )

        ApiDSL.clear_world(self)
        ApiDSL.When_i_access_advertisement_with(self, place=website_place)
        ApiDSL.Then_i_should_receive_success_response(self)
        results = self.world.get('content').get('results')
        ApiDSL.Then_i_should_see_result_list(self, num=1)

        results = self.world.get('content').get('results')
        self.assertEqual(adv1.title, results[0].get('title'))



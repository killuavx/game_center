# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.reverse import reverse
from ranking.models import PackageRanking
from mobapi2.serializers import HyperlinkedModelSerializer
from mobapi2.warehouse.serializers.package import PackageSummarySerializer


class PackageRankingSummarySerializer(HyperlinkedModelSerializer):

    CHOICE_CYCLE_TYPE = dict(list(zip(dict(PackageRanking.CYCLE_TYPES).values(),
                                      dict(PackageRanking.CYCLE_TYPES).keys())))

    ranking_name = serializers.RelatedField(source='ranking_type.title')

    ranking_slug = serializers.RelatedField(source='ranking_type.slug')

    category_slug = serializers.RelatedField(source='category.slug')

    category_name = serializers.RelatedField(source='category.name')

    cycle_type = serializers.SerializerMethodField('get_cycle_type')
    def get_cycle_type(self, obj):
        return obj.get_cycle_type_display()

    limit_packages = 5
    serializer_class_package = PackageSummarySerializer
    packages = serializers.SerializerMethodField('get_packages')
    def get_packages(self, obj):
        packages = obj.packages.published()[0:self.limit_packages]
        return PackageSummarySerializer(packages,
                                        many=True,
                                        context=self.context).data

    packages_url = serializers.SerializerMethodField('get_packages_url')
    def get_packages_url(self, obj):
        viewname = 'ranking-packages'
        reverse_viewname = self.opts.router.get_base_name(viewname)
        request = self.context.get('request')
        path = reverse(reverse_viewname,
                       kwargs=dict(pk=obj.pk),
                       request=request)
        return path

    def get_default_fields(self):
        self.opts.view_name = self.opts.router.get_base_name(self.opts.view_name)
        return super(PackageRankingSummarySerializer, self) \
            .get_default_fields()

    class Meta:
        model = PackageRanking
        view_name = 'ranking-detail'
        fields = (
            'url',
            'ranking_name',
            'ranking_slug',
            'category_slug',
            'category_name',
            'packages',
            'packages_url',
            'cycle_type',
        )


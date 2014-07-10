# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db.models import Sum, Count
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import get_default_timezone, get_current_timezone
from django.views.generic.list import ListView
from django.core import exceptions
from django.utils.timezone import now, timedelta
from dateutil import parser as dateparser

from analysis.models import (
    SumActivateDeviceProductChannelPackageResult,
    DateDim, DevicePlatformDim,
    SumActivateDeviceProductChannelResult,
    PLATFORM_CHOICES, PLATFORM_DEFAULT,
    ProductDim, ProductKeyDim,
    CubeDownloadProductPackageIncomingResult,
    CubeActivateDeviceProductChannelPackageResult,
    PackageKeyDim)


class BaseFilterBackend(object):

    def filter_queryset(self, request, queryset, view):
        """
        Return a filtered queryset.
        """
        raise NotImplementedError(".filter_queryset() must be overridden.")


class OrderingFitler(BaseFilterBackend):

    ordering_param = 'ordering'

    def get_ordering(self, view):
        ordering = getattr(view, self.ordering_param, None)
        if isinstance(ordering, str):
            return (ordering,)
        return ordering

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(view)
        if ordering:
            return queryset.order_by(*ordering)

        return queryset


class FilterViewMixin(object):

    filter_backends = ()

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.

        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        filter_backends = self.filter_backends or []
        for backend in filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class BaseListView(FilterViewMixin, ListView):

    paginate_by = 20

    def get_queryset(self):
        qs = super(BaseListView, self).get_queryset()
        return self.filter_queryset(qs)

    def get(self, request, *args, **kwargs):
        self.request = request
        self.query_args = args
        self.query_kwargs = kwargs
        return super(BaseListView, self).get(request=request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseListView, self).get_context_data(**kwargs)
        context.update(query=self.query_kwargs)
        return context

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseListView, self).dispatch(*args, **kwargs)


def set_view_dim_to_query_kwargs(view, name, obj):
    if 'dims' not in view.query_kwargs:
        view.query_kwargs['dims'] = dict()
    view.query_kwargs['dims'][name] = obj


class StartEndDateDimFilterBackend(BaseFilterBackend):

    start_date_param = 'start_date'

    end_date_param = 'end_date'

    def get_datedim(self, view, name):
        dd = None
        if name in view.query_kwargs and view.query_kwargs.get(name):
            try:
                dt = dateparser.parse(view.query_kwargs.get(name))
                dd = DateDim.objects.get_by_datetime(dt)
            except ValueError as e:
                raise exceptions.ValidationError(str(e))
            except exceptions.ObjectDoesNotExist as e:
                raise exceptions.ValidationError(str(e))
        return dd

    def get_yesterday_datedim(self):
        yesterday = now().astimezone() - timedelta(days=1)
        return DateDim.objects.get_by_datetime(yesterday)

    def get_latest_datedim(self, queryset):
        day = queryset \
                   .dates("%s__datevalue" % self.start_date_param, 'day', 'DESC')[0]
        return DateDim.objects.get_by_datetime(day)

    def filter_queryset(self, request, queryset, view):
        sd = self.get_datedim(view, self.start_date_param)
        ed = self.get_datedim(view, self.end_date_param)
        if not sd:
            #sd = self.get_yesterday_datedim()
            sd = self.get_latest_datedim(queryset)
            view.query_kwargs[self.start_date_param] = sd.datevalue.strftime('%Y-%m-%d')
        if not ed:
            ed = sd
        qs = queryset.filter(start_date=sd, end_date=ed)
        return qs


class PlatformDimFilterBackend(BaseFilterBackend):

    platform_param = 'device_platform'

    PLATFORM_LIST = list(dict(PLATFORM_CHOICES).keys())

    def filter_queryset(self, request, queryset, view):
        platform = view.query_kwargs.get('platform')
        if platform not in self.PLATFORM_LIST:
            platform = PLATFORM_DEFAULT
        dp = DevicePlatformDim.objects.get(platform=platform)
        lookup = {self.platform_param: dp}
        return queryset.filter(**lookup)


def factory_filterbackend_from_request_get(filterbackend, **kwargs):

    class base_class(filterbackend):

        def filter_queryset(self, request, queryset, view):
            for lookup_field, query_dict_name in kwargs.items():
                val = request.GET.get(query_dict_name)
                view.query_kwargs[lookup_field] = val
            return super(base_class, self).filter_queryset(request, queryset, view)

    class_name = "GetQuery%s" % filterbackend.__class__.__name__
    class_attrs = {
        '__module__': filterbackend.__module__
    }
    return type(base_class)(class_name, (base_class,), class_attrs)


class ProductDimFilterBackend(BaseFilterBackend):

    entrytype_param = 'entrytype'

    channel_param = 'channel'

    def filter_queryset(self, request, queryset, view):
        lookup_dict = {
            'entrytype': view.query_kwargs.get(self.entrytype_param),
            'channel': view.query_kwargs.get(self.channel_param)
        }
        pd = ProductDim.objects.get(**lookup_dict)
        set_view_dim_to_query_kwargs(view, 'product', pd)
        return queryset.filter(product=pd)


class ProductKeyDimFilterBackend(BaseFilterBackend):

    entrytype_param = 'entrytype'

    def filter_queryset(self, request, queryset, view):
        lookup_dict = {
            'entrytype': view.query_kwargs.get(self.entrytype_param),
        }
        pkd = ProductKeyDim.objects.get(**lookup_dict)
        set_view_dim_to_query_kwargs(view, 'productkey', pkd)
        return queryset.filter(productkey=pkd)


class CycleTypeFilterBackend(BaseFilterBackend):

    cycle_type_param = 'cycle_type'

    def filter_queryset(self, request, queryset, view):
        cycle_type = view.query_kwargs.get(self.cycle_type_param)
        if cycle_type and cycle_type in list(dict(view.model.CYCLE_TYPES).keys()):
            return queryset.filter(cycle_type=cycle_type)
        return queryset


class ProductActivateListView(BaseListView):

    template_name = 'analysis/admin/pages/product.html'

    #model = SumActivateDeviceProductResult
    model = SumActivateDeviceProductChannelPackageResult

    filter_backends = (
        PlatformDimFilterBackend,
        CycleTypeFilterBackend,
        StartEndDateDimFilterBackend,
    )

    def get_result_total(self):
        group_fields = ('device_platform',)
        sum_fields = ('total_reserve_count',
                      'reserve_count',
                      'active_count',
                      'open_count', )
        querydict = {f:Sum(f) for f in sum_fields}

        queryset = self.model.objects.all()
        queryset = PlatformDimFilterBackend()\
            .filter_queryset(self.request, queryset, self)
        queryset = StartEndDateDimFilterBackend()\
            .filter_queryset(self.request, queryset, self)
        qs = queryset.values(*group_fields) \
            .order_by(*group_fields).annotate(**querydict)
        try:
            return qs.get()
        except exceptions.ObjectDoesNotExist:
            return dict(zip(sum_fields, len(sum_fields) * [0]))

    def get_context_data(self, **kwargs):
        context = super(ProductActivateListView, self).get_context_data(**kwargs)
        context['total_result'] = self.get_result_total()
        return context

    def get(self, request, *args, **kwargs):
        kwargs.setdefault('platform', request.GET.get('platform', PLATFORM_DEFAULT))
        kwargs.setdefault('start_date', request.GET.get('start_date'))
        kwargs.setdefault('end_date', request.GET.get('end_date'))
        return super(ProductActivateListView, self).get(request, *args, **kwargs)


class ProductChannelActivateListView(BaseListView):

    template_name = 'analysis/admin/pages/product_channel.html'

    model = SumActivateDeviceProductChannelPackageResult

    filter_backends = (
        PlatformDimFilterBackend,
        ProductKeyDimFilterBackend,
        StartEndDateDimFilterBackend,
    )

    def get_context_data(self, **kwargs):
        context = super(ProductChannelActivateListView, self).get_context_data(**kwargs)
        context['productkey'] = ProductKeyDim.objects\
            .get(entrytype=self.query_kwargs.get('entrytype'))
        return context

    def get(self, request, entrytype=None, *args, **kwargs):
        kwargs.setdefault('entrytype', entrytype)
        kwargs.setdefault('platform', request.GET.get('platform', PLATFORM_DEFAULT))
        kwargs.setdefault('start_date', request.GET.get('start_date'))
        kwargs.setdefault('end_date', request.GET.get('end_date'))
        response = super(ProductChannelActivateListView, self).get(request, *args, **kwargs)
        return response


class ProductChannelCycleActivateListView(BaseListView):

    template_name = 'analysis/admin/pages/product_channel_detail.html'

    model = SumActivateDeviceProductChannelPackageResult

    filter_backends = (
        PlatformDimFilterBackend,
        ProductDimFilterBackend,
        CycleTypeFilterBackend,
    )

    def get_context_data(self, **kwargs):
        context = super(ProductChannelCycleActivateListView, self).get_context_data(**kwargs)
        context['product'] = ProductDim.objects \
            .get(entrytype=self.query_kwargs.get('entrytype'),
                 channel=self.query_kwargs.get('channel'))
        return context

    def get(self, request, entrytype=None, channel=None, *args, **kwargs):
        kwargs.setdefault('platform', request.GET.get('platform', PLATFORM_DEFAULT))
        kwargs.setdefault('entrytype', entrytype)
        kwargs.setdefault('channel', channel)
        kwargs.setdefault('cycle_type', 1)
        kwargs.setdefault('start_date', request.GET.get('start_date'))
        kwargs.setdefault('end_date', request.GET.get('end_date'))
        response = super(ProductChannelCycleActivateListView, self).get(request, *args, **kwargs)
        return response


from rest_framework.filters import SearchFilter as _SearchFilter


class SearchFilterBackend(_SearchFilter):

    search_param = 'q'

    def get_search_terms(self, request):
        params = request.REQUEST.get(self.search_param, '')
        return params.replace(',', ' ').split()


class PackageDownloadListView(BaseListView):

    template_name = 'analysis/admin/pages/download_package.html'

    model = CubeDownloadProductPackageIncomingResult

    sum_fields = ('download_count',
                  'total_download_count',
                  'downloaded_count',
                  'total_downloaded_count',)

    class GroupPackageFilterBackend(BaseFilterBackend):

        def filter_queryset(self, request, queryset, view):
            group_fields = ('device_platform', 'download_packagekey', )
            querydict = {f:Sum(f) for f in PackageDownloadListView.sum_fields}
            qs = queryset.values(*group_fields).order_by(*group_fields).annotate(**querydict)
            return qs

    filter_backends = (
        PlatformDimFilterBackend,
        CycleTypeFilterBackend,
        StartEndDateDimFilterBackend,
        GroupPackageFilterBackend,
        SearchFilterBackend,
    )

    search_fields = ('download_packagekey__package_name',
                     'download_packagekey__title')

    def get_result_total(self):
        group_fields = ('device_platform',)
        querydict = {f:Sum(f) for f in self.sum_fields}

        queryset = self.model.objects.all()
        queryset = PlatformDimFilterBackend() \
            .filter_queryset(self.request, queryset, self)
        queryset = StartEndDateDimFilterBackend() \
            .filter_queryset(self.request, queryset, self)
        qs = queryset.values(*group_fields) \
            .order_by(*group_fields).annotate(**querydict)
        try:
            return qs.get()
        except exceptions.ObjectDoesNotExist:
            return dict(zip(self.sum_fields, len(self.sum_fields) * [0]))

    def get_context_data(self, **kwargs):
        context = super(PackageDownloadListView, self).get_context_data(**kwargs)
        platform = self.query_kwargs.get('platform')
        device_platform = DevicePlatformDim.objects.get(platform=platform)
        for item in context['object_list']:
            item['device_platform'] = device_platform
            item['download_packagekey'] = PackageKeyDim.objects.get(pk=item['download_packagekey'])

        context['total_result'] = self.get_result_total()
        return context

    def get(self, request, *args, **kwargs):
        kwargs.setdefault('platform', request.GET.get('platform', PLATFORM_DEFAULT))
        kwargs.setdefault('cycle_type', 1)
        kwargs.setdefault('start_date', request.GET.get('start_date'))
        kwargs.setdefault('end_date', request.GET.get('end_date'))
        kwargs.setdefault('q', request.GET.get('q'))
        return super(PackageDownloadListView, self).get(request, *args, **kwargs)


class DownloadPackageKeyFilterBackend(BaseFilterBackend):

    platform_param = 'platform'

    packagekey_param = 'package_name'

    lookup_packagekey_param = 'download_packagekey'

    def filter_queryset(self, request, queryset, view):
        package_name = view.query_kwargs.get(self.packagekey_param)
        platform = view.query_kwargs.get(self.platform_param)
        if package_name:
            try:
                pkd = PackageKeyDim.objects.get(platform=platform,
                                                package_name=package_name)
                set_view_dim_to_query_kwargs(view, 'download_packagekey', pkd)
            except PackageKeyDim.DoesNotExist:
                return queryset.none()

            return queryset.filter(**{self.lookup_packagekey_param: pkd})
        return queryset


class ProductPackageDownloadListView(BaseListView):

    template_name = 'analysis/admin/pages/download_package_detail.html'

    model = CubeDownloadProductPackageIncomingResult

    filter_backends = (
        PlatformDimFilterBackend,
        DownloadPackageKeyFilterBackend,
        CycleTypeFilterBackend,
        OrderingFitler,
    )

    ordering = ('-start_date', )

    def get_context_data(self, **kwargs):
        context = super(ProductPackageDownloadListView, self).get_context_data(**kwargs)
        context['packagekey'] = PackageKeyDim.objects\
            .get(platform=self.query_kwargs.get('platform'),
                 package_name=self.query_kwargs.get('package_name'))
        return context

    def get(self, request, *args, **kwargs):
        kwargs.setdefault('platform', request.GET.get('platform', PLATFORM_DEFAULT))
        kwargs.setdefault('cycle_type', 1)
        kwargs.setdefault('start_date', request.GET.get('start_date'))
        kwargs.setdefault('end_date', request.GET.get('end_date'))
        return super(ProductPackageDownloadListView, self).get(request, *args, **kwargs)

from warehouse.models import Package, PackageVersion
from taxonomy.models import Category


class PackageProxy(Package):

    def admin_url(self):
        view_name = 'admin:%s_%s_change' % (Package._meta.app_label,
                                            Package._meta.module_name)
        link = reverse(view_name, args=[self.pk])
        return link

    def version_admin_url(self):
        latest_version = self.latest_version()
        view_name = 'admin:%s_%s_change' % (PackageVersion._meta.app_label,
                                            PackageVersion._meta.module_name)
        link = reverse(view_name, args=[latest_version.pk])
        return link

    def latest_version(self):
        if not hasattr(self, '_latest_verison'):
            self._latest_version = self.versions.latest('version_code')
        return self._latest_version

    class Meta:
        proxy = True


class CrackCategoryFilterBackend(BaseFilterBackend):

    crack_slug = 'crack-game'

    def filter_queryset(self, request, queryset, view):
        cat = Category.objects.get(slug=self.crack_slug)
        return queryset.filter(categories__in=[cat])


class CrackPackageRelasedFilterBackend(BaseFilterBackend):

    released_datetime__param = 'start_date'

    def filter_queryset(self, request, queryset, view):
        released_dt = view.query_kwargs.get(self.released_datetime__param)
        if not released_dt:
            return queryset
        dt = dateparser.parse(released_dt)
        dt = dt.replace(tzinfo=get_current_timezone())
        end_dt = dt + timedelta(days=1)
        return queryset.filter(released_datetime__gte=dt, released_datetime__lt=end_dt)


class CrackPackageListView(BaseListView):

    template_name = 'analysis/admin/pages/crack_package.html'

    model = PackageProxy

    filter_backends = (
        CrackCategoryFilterBackend,
        SearchFilterBackend,
        CrackPackageRelasedFilterBackend,
        OrderingFitler,
    )

    search_fields = ('package_name', 'title', )

    ordering = ('-released_datetime', )

    def get_total_result(self):
        result = dict(version_count=0, package_count=0)
        queryset = self.model.objects.all().values('pk')

        queryset = CrackCategoryFilterBackend().filter_queryset(self.request, queryset, self)
        for fb in self.filter_backends:
            if fb is OrderingFitler:
                continue
            queryset = fb().filter_queryset(self.request, queryset, self)

        result['package_count'] = queryset.count()
        sql = 'SELECT COUNT(id) as cnt FROM %s WHERE package_id=%s.id'
        qs = queryset\
            .extra(select={'version_count': sql %(PackageVersion._meta.db_table,
                                                  Package._meta.db_table)})\
            .annotate(version_count=Count('versions'))
        sum_version_count = 0
        for p in qs:
            sum_version_count += p['version_count']

        result['version_count'] = sum_version_count
        return result

    def get_context_data(self, **kwargs):
        context = super(CrackPackageListView, self).get_context_data(**kwargs)
        context['total_result'] = self.get_total_result()
        return context

    def get(self, request, *args, **kwargs):
        kwargs.setdefault('platform', request.GET.get('platform', PLATFORM_DEFAULT))
        kwargs.setdefault('start_date', request.GET.get('start_date'))
        kwargs.setdefault('q', request.GET.get('q'))
        return super(CrackPackageListView, self).get(request, *args, **kwargs)


class BetweenStartEndDateDimFilterBackend(StartEndDateDimFilterBackend):

    def filter_queryset(self, request, queryset, view):
        sd = self.get_datedim(view, self.start_date_param)
        ed = self.get_datedim(view, self.end_date_param)
        if not sd:
            return queryset
        if not ed:
            ed = sd
        qs = queryset.filter(start_date_id__gte=sd.pk, start_date__lt=ed)
        return qs


class DownloadPackageKeyIgnorePlatformFilterBackend(BaseFilterBackend):

    packagekey_param = 'package_name'

    lookup_packagekey_param = 'download_packagekey__package_name'

    def filter_queryset(self, request, queryset, view):
        package_name = view.query_kwargs.get(self.packagekey_param)
        if package_name:
            return queryset.filter(**{self.lookup_packagekey_param: package_name})
        return queryset


class CrackPackageDownloadListView(BaseListView):

    template_name = 'analysis/admin/pages/crack_package_download_detail.html'

    model = CubeDownloadProductPackageIncomingResult

    filter_backends = (
        DownloadPackageKeyIgnorePlatformFilterBackend,
        CycleTypeFilterBackend,
        BetweenStartEndDateDimFilterBackend,
        OrderingFitler,
    )

    ordering = ('-start_date', 'device_platform', 'productkey', )

    def get_context_data(self, **kwargs):
        context = super(CrackPackageDownloadListView, self).get_context_data(**kwargs)
        context['package'] = PackageProxy.objects \
            .get(package_name=self.query_kwargs.get('package_name'))
        return context

    def get(self, request, package_name=None, *args, **kwargs):
        kwargs.setdefault('cycle_type', 1)
        kwargs.setdefault('package_name', package_name)
        kwargs.setdefault('start_date', request.GET.get('start_date'))
        kwargs.setdefault('end_date', request.GET.get('end_date'))
        return super(CrackPackageDownloadListView, self).get(request, *args, **kwargs)


class PackageKeyDimIgnorePlatformFilterBackend(BaseFilterBackend):

    packagekey_param = 'package_name'

    def filter_queryset(self, request, queryset, view):
        package_name = view.query_kwargs.get(self.packagekey_param)
        if not package_name:
            return queryset
        _ids = list(PackageKeyDim.objects.filter(package_name=package_name).values_list('pk', flat=True))
        if not _ids:
            return queryset.none()
        return queryset.filter(packagekey_id__in=_ids)


class CrackPackageActivateListView(BaseListView):

    template_name = 'analysis/admin/pages/crack_package_activate_list.html'

    model = CubeActivateDeviceProductChannelPackageResult

    filter_backends = (
        CycleTypeFilterBackend,
        PackageKeyDimIgnorePlatformFilterBackend,
        StartEndDateDimFilterBackend,
        OrderingFitler,
    )
    ordering = ('productkey', 'product', )

    def get_context_data(self, **kwargs):
        context = super(CrackPackageActivateListView, self).get_context_data(**kwargs)
        context['package'] = PackageProxy.objects \
            .get(package_name=self.query_kwargs.get('package_name'))
        return context

    def get(self, request, package_name=None, *args, **kwargs):
        kwargs.setdefault('cycle_type', 1)
        kwargs.setdefault('package_name', package_name)
        kwargs.setdefault('start_date', request.GET.get('start_date'))
        kwargs.setdefault('end_date', request.GET.get('end_date'))
        return super(CrackPackageActivateListView, self).get(request, *args, **kwargs)


class CrackPackageChannelActivateListView(BaseListView):

    template_name = 'analysis/admin/pages/crack_package_activate_detail.html'

    model = CubeActivateDeviceProductChannelPackageResult

    filter_backends = (
        CycleTypeFilterBackend,
        ProductDimFilterBackend,
        ProductKeyDimFilterBackend,
        PackageKeyDimIgnorePlatformFilterBackend,
        BetweenStartEndDateDimFilterBackend,
        OrderingFitler,
    )
    ordering = ('productkey', 'product', )

    def get_context_data(self, **kwargs):
        context = super(CrackPackageChannelActivateListView, self).get_context_data(**kwargs)
        context['package'] = PackageProxy.objects \
            .get(package_name=self.query_kwargs.get('package_name'))
        return context

    def get(self, request, package_name=None, entrytype=None, channel=None, *args, **kwargs):
        kwargs.setdefault('platfrom', PLATFORM_DEFAULT)
        kwargs.setdefault('channel', channel)
        kwargs.setdefault('entrytype', entrytype)

        kwargs.setdefault('cycle_type', 1)
        kwargs.setdefault('package_name', package_name)
        kwargs.setdefault('start_date', request.GET.get('start_date'))
        kwargs.setdefault('end_date', request.GET.get('end_date'))
        return super(CrackPackageChannelActivateListView, self).get(request, *args, **kwargs)

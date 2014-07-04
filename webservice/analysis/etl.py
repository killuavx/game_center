# -*- coding: utf-8 -*-
from django.core.exceptions import MultipleObjectsReturned
from django.db import IntegrityError
from django.db import transaction
from .models import *
from .documents.event import Event
from mongoengine import Q
from django.utils.timezone import datetime, timedelta, get_default_timezone
from dateutil.relativedelta import *
import logging
from analysis.helpers import *

USING = UsinglogFact.objects.db

logger = logging.getLogger('scripts')


class ExtractDimensionTask(object):

    logger = logger

    dimension_class = None

    is_started = False

    is_finished = False

    map_func = None

    reduce_func = """
    function(key, values){
        reduce_value = values[0];
        reduce_value._id = ObjectId();
        return reduce_value;
    }
    """

    def __init__(self, queryset):
        self.queryset = queryset

    def filter_queryset(self, queryset):
        return queryset

    def execute(self):
        self.logger.info('START %s' % self.__class__)
        self.is_started = True
        self.logger.info('Extract Mapreduce %s' % self.__class__)
        result = self.extract_mapreduce(self.queryset)
        self.logger.info('Transfrom to db %s' % self.__class__)
        self.trans_to_db(result)
        self.is_finished = True
        self.logger.info('END %s' % self.__class__)

    def extract_mapreduce(self, queryset):
        map_func, reduce_func = self.get_mapreduce_functions()
        queryset = self.filter_queryset(queryset)
        queryset = queryset.timeout(False)
        return queryset.map_reduce(map_func,
                                   reduce_func,
                                   output=self.dimension_class._meta.db_table)

    def get_mapreduce_functions(self):
        raise NotImplementedError()

    def trans_to_db(self, iterator):
        for doc in iterator:
            kwvals = dict(doc.value)
            self.get_or_create_dimension(kwvals)

    @classmethod
    def get_or_create_dimension(cls, val):
        raise NotImplementedError()


class ExtractEventDimensionTask(ExtractDimensionTask):

    dimension_class = EventDim

    def get_mapreduce_functions(self):
        map_func = """function(){
            emit(this.eventtype, {eventtype: this.eventtype});
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        defaults = dict(eventtype=val.get('eventtype'))
        return cls.dimension_class.objects \
            .get_or_create(defaults=defaults, **defaults)


class ExtractProductDimensionTask(ExtractDimensionTask):

    dimension_class = ProductDim

    def get_mapreduce_functions(self):
        map_func = """
        function(){
            var key = [this.entrytype, this.channel].join(" ");
            var value = {entrytype: this.entrytype,
                         channel: this.channel};
            emit(key, value);
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        defaults = dict(entrytype=val.get('entrytype'),
                        channel=val.get('channel') or UNDEFINED)
        return cls.dimension_class.objects \
            .get_or_create(defaults=defaults, **defaults)


class ExtractPackageDimensionTask(ExtractDimensionTask):

    dimension_class = PackageDim


    def get_mapreduce_functions(self):
        map_func = """
        function(){
            var key = [this.package_name, this.version_name, this.platform].join(" ");
            var value = {package_name: this.package_name,
                         version_name: this.version_name,
                         platform: this.platform};
            emit(key, value);
            if(['download', 'downloaded'].indexOf(this.eventtype) != -1 ){
                key = [this.download_package_name,
                       this.download_version_name,
                       this.platform].join(" ");
                value = {package_name: this.download_package_name,
                         version_name: this.download_version_name,
                         platform: this.platform};
                emit(key, value);
            }
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        lookup = dict(package_name=val.get('package_name') or UNDEFINED,
                      version_name=val.get('version_name') or UNDEFINED,
                      platform=val.get('platform') or PLATFORM_DEFAULT)
        obj, created = cls.dimension_class.objects\
            .get_or_create(**lookup)
        if created or not obj.pid:
            obj = packagecategorydim_fill_to(obj)
            obj = packageversion_id_fill(obj)
            obj.save()

        # packagekey_dim
        pk_obj, pk_created = PackageKeyDim.objects\
            .get_or_create_from_package_dim(obj)

        return obj, created


def packagecategorydim_fill_to(pkg_or_ver_dim):
    obj = pkg_or_ver_dim
    cats = find_platform_categories(obj.platform, obj)
    if cats:
        root_cat, primary_cat, second_cat = cats
        if root_cat:
            obj.root_category, created = packagecategorydim_get_or_category_from(root_cat)
        if primary_cat:
            obj.primary_category, created = packagecategorydim_get_or_category_from(primary_cat)
        if second_cat:
            obj.second_category, created = packagecategorydim_get_or_category_from(second_cat)
    return obj


def packagecategorydim_get_or_category_from(category):
    if not category:
        return None, None
    obj, created = PackageCategoryDim.objects.get_or_create(
        cid=category.pk,
        slug=category.slug,
        defaults=dict(
            name=category.name
        )
    )
    if obj.name != category.name:
        category.name = obj.name
        category.save()
    return obj, created


class ExtractSubscriberIdDimensionTask(ExtractDimensionTask):

    dimension_class = SubscriberIdDim

    def get_mapreduce_functions(self):
        map_func = """function(){
            var mnc = this.cell && this.cell.mnc;
            var key = this.imsi;
            var value = {imsi: this.imsi,
                         mnc: mnc };
            emit(key, value);
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        mnc = val.get('mnc')
        if str(mnc).isnumeric():
            mnc = "%02d" % mnc
        else:
            mnc = UNDEFINED
        imsi = imsi=val.get('imsi') or UNDEFINED
        defaults = dict(imsi=imsi, mnc=mnc)
        return cls.dimension_class.objects\
            .get_or_create(imsi=imsi, defaults=defaults)


class ExtractDeviceDimensionTask(ExtractDimensionTask):

    dimension_class = DeviceDim

    def get_mapreduce_functions(self):
        map_func = """
        function(){
            if(this.imei == '') this.imei = null;
            var key = this.imei;
            var value = {imei: key,
                         platform: this.platform };
            emit(key, value);
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        imei = val.get('imei') or UNDEFINED
        defaults = dict(imei=imei, platform=val.get('platform') or PLATFORM_DEFAULT)
        return cls.dimension_class.objects.get_or_create(imei=imei,
                                                         defaults=defaults)


class ExtractDevicePlatformDimensionTask(ExtractDimensionTask):

    dimension_class = DevicePlatformDim

    def get_mapreduce_functions(self):
        map_func = """
        function(){
            var key = this.platform;
            var value = {platform: this.platform };
            emit(key, value);
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        defaults=dict(platform=val.get('platform') or PLATFORM_DEFAULT)
        return cls.dimension_class.objects\
            .get_or_create(defaults=defaults, **defaults)


class ExtractDeviceOSDimensionTask(ExtractDimensionTask):

    dimension_class = DeviceOSDim

    def get_mapreduce_functions(self):
        map_func = """
        function(){
            var key = [this.platform, this.os_version].join(" ");
            var value = {platform: this.platform,
                         os_version: this.os_version };
            emit(key, value);
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        defaults = dict(platform=val.get('platform') or PLATFORM_DEFAULT,
                        os_version=val.get('os_version') or UNDEFINED)
        return cls.dimension_class.objects\
            .get_or_create(defaults=defaults, **defaults)


class ExtractDeviceResolutionDimensionTask(ExtractDimensionTask):

    dimension_class = DeviceResolutionDim

    def get_mapreduce_functions(self):
        map_func = """
        function(){
            var key = this.resolution;
            var val = {resolution: this.resolution};
            emit(key, val);
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        orig_resolution = val.get('resolution') or UNDEFINED
        return cls.dimension_class.objects \
            .get_or_create_by_orig_resolution(orig_resolution)


class ExtractDeviceModelDimensionTask(ExtractDimensionTask):

    dimension_class = DeviceModelDim

    def get_mapreduce_functions(self):
        map_func = """
        function(){
            var key = [this.manufacturer,
                       this.device_name,
                       this.module_name,
                       this.model_name].join("|");
            var value = {manufacturer: this.manufacturer,
                         device_name: this.device_name,
                         module_name: this.module_name,
                         model_name: this.model_name }
            emit(key, value);
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        defaults = dict(manufacturer=val.get('manufacturer') or UNDEFINED,
                        device_name=val.get('device_name') or UNDEFINED,
                        module_name=val.get('module_name') or UNDEFINED,
                        model_name=val.get('model_name') or UNDEFINED)
        return cls.dimension_class.objects\
            .get_or_create(defaults=defaults, **defaults)


class ExtractDeviceSupplierDimensionTask(ExtractDimensionTask):

    dimension_class = DeviceSupplierDim

    def get_mapreduce_functions(self):
        map_func = """
        function(){
            var mcc = this.cell && this.cell.mcc;
            var mnc = this.cell && this.cell.mnc;
            var key = [String(mcc), String(mnc)].join("");
            if(typeof(mcc) == "undefined" || typeof(mnc) == "undefined"){
                key = null;
            }
            var value = {mccmnc: key,
                         country_code: String(mcc),
                         cell: this.cell,
                         mcc: mcc,
                         mnc: mnc
                         };
            emit(key, value);
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        if 'cell' in val:
            val = val.get('cell') or dict()
        mnc = val.get('mnc')
        country_code = val.get('mcc') or UNDEFINED
        if str(mnc).isnumeric():
            mnc = "%02d" % mnc
        else:
            mnc = UNDEFINED
        if UNDEFINED in (mnc, country_code):
            mccmnc = UNDEFINED
        else:
            mccmnc = "%s%s" %(country_code, mnc)

        defaults = dict(mccmnc=mccmnc, country_code=country_code)
        return cls.dimension_class.objects.get_or_create(mccmnc=mccmnc,
                                                         defaults=defaults)


class ExtractDeviceLanguageDimensionTask(ExtractDimensionTask):

    dimension_class = DeviceLanguageDim

    def get_mapreduce_functions(self):
        map_func = """
        function(){
            var key = this.language;
            var value = {language: this.language };
            emit(key, value);
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        defaults = dict(language=val.get('language') or UNDEFINED)
        return cls.dimension_class.objects\
            .get_or_create(defaults=defaults, **defaults)


class ExtractNetworkDimensionTask(ExtractDimensionTask):

    dimension_class = NetworkDim

    def get_mapreduce_functions(self):
        map_func = """
        function(){
            var key = this.network;
            var value = {network: this.network};
            emit(key, value);
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        defaults = dict(network=val.get('network') or UNDEFINED)
        return cls.dimension_class.objects\
            .get_or_create(defaults=defaults, **defaults)


class ExtractPageDimensionTask(ExtractDimensionTask):

    dimension_class = PageDim

    def get_mapreduce_functions(self):
        map_func = """function(){
            emit(this.page_name, {page_name: this.page_name, is_url:false});
            if(this.referer){
                emit(this.referer, {page_name: this.referer, is_url:true});
            }
            if(this.current_uri){
                emit(this.current_uri, {page_name: this.current_uri, is_url:true});
            }
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        page_name = val.get('page_name') or UNDEFINED
        try:
            obj = cls.dimension_class.objects.get(urlvalue=page_name)
            return obj, False
        except cls.dimension_class.DoesNotExist:
            obj = cls.dimension_class()
            if val.get('is_url'):
                obj.page_url = page_name
                obj.is_url = True
            else:
                obj.urlvalue = page_name
                obj.is_url = False
            obj.save()
            return obj, True


class ExtractMediaUrlDimensionTask(ExtractDimensionTask):

    dimension_class = MediaUrlDim

    def filter_queryset(self, queryset):
        return queryset.filter(eventtype__in=['download', 'downloaded'])

    def get_mapreduce_functions(self):
        map_func = """function(){
            emit(this.current_uri, {page_name: this.current_uri, is_url:true});
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        page_name = val.get('page_name') or UNDEFINED
        if page_name == UNDEFINED:
            return cls.dimension_class.objects.get_or_create(urlvalue=page_name)
        else:
            return cls.dimension_class.objects\
                .get_or_create_by_page_url(page_url=page_name)


class ExtractBaiduPushDimensionTask(ExtractDimensionTask):

    dimension_class = BaiduPushDim

    def get_mapreduce_functions(self):
        map_func = """function(){
            var val = {channel_id: this.baidu_push_channel_id,
                       user_id: this.baidu_push_user_id,
                       app_id: this.baidu_push_app_id,
                       baidu_push_channel_id: this.baidu_push_channel_id,
                       baidu_push_user_id: this.baidu_push_user_id,
                       baidu_push_app_id: this.baidu_push_app_id
                       };
            var key = val.channel_id && val.user_id && val.app_id && [val.channel_id,
                                                                      val.user_id,
                                                                      val.app_id].join(" ");
            emit(key, val);
        }
        """
        return map_func, self.reduce_func

    @classmethod
    def get_or_create_dimension(cls, val):
        defaults = dict(channel_id=val.get('channel_id') or val.get('baidu_push_channel_id') or UNDEFINED,
                        user_id=val.get('user_id') or val.get('baidu_push_user_id') or UNDEFINED,
                        app_id=val.get('app_id') or val.get('baidu_push_app_id') or UNDEFINED)
        return cls.dimension_class.objects.get_or_create(defaults=defaults,
                                                         **defaults)


# ETL
class ETLProcessor(object):

    logger = logger

    extract_classes = (
        ExtractEventDimensionTask,
        ExtractProductDimensionTask,
        ExtractPackageDimensionTask,
        ExtractPageDimensionTask,
        ExtractMediaUrlDimensionTask,
        ExtractSubscriberIdDimensionTask,
        ExtractDeviceDimensionTask,
        ExtractDevicePlatformDimensionTask,
        ExtractDeviceOSDimensionTask,
        ExtractDeviceResolutionDimensionTask,
        ExtractDeviceModelDimensionTask,
        ExtractDeviceSupplierDimensionTask,
        ExtractDeviceLanguageDimensionTask,
        ExtractNetworkDimensionTask,
        ExtractBaiduPushDimensionTask,
    )

    def get_doc_queryset(self):
        return Event.objects

    def get_doc_queryset_between(self, start_date, end_date):
        tz = get_default_timezone()
        s_date = make_aware(start_date, tz) if not is_aware(start_date) else start_date
        e_date = make_aware(end_date, tz) if not is_aware(end_date) else end_date
        return self.get_doc_queryset() \
            .filter(created_datetime__gte=s_date,
                    created_datetime__lt=e_date)

    def process_between(self, start_date, end_date):
        queryset = self.get_doc_queryset_between(start_date, end_date)
        self.extract_to_dimensions(queryset)
        self.transform_to_fact(queryset)

    # Extract Dimensions
    def extract_to_dimensions(self, queryset):
        """
        抽取维度数据
        """
        for ecls in self.extract_classes:
            etask = ecls(queryset)
            etask.execute()

    # Transform Fact
    def transform_to_fact(self, queryset):
        """
        转移事实数据
        """
        raise NotImplementedError()


class UsinglogETLProcessor(ETLProcessor):

    def transform_to_fact(self, queryset):
        qf = Q(is_transformed_fact__exists=False) | Q(is_transformed_fact=False)
        queryset = queryset.filter(qf).order_by('created_datetime')
        doc_count = 0
        created_count = 0
        for doc in queryset.timeout(False):
            doc_count += 1
            try:
                sid = transaction.savepoint(USING)
                UsinglogFact.objects.create_by_doc(doc)
                transaction.savepoint_commit(sid)
                created_count += 1
            except IntegrityError as e:
                transaction.savepoint_rollback(sid)
                msg = "%s, %s" % (str(e), doc._data)
                self.logger.warning(msg)
                if not hasattr(doc, 'is_transformed_fact'):
                    doc.is_transformed_fact = True
                    doc.save()
            else:
                doc.is_transformed_fact = True
                doc.save()
            msg = "%s/%s %s" %(created_count, doc_count, doc.created_datetime)
            self.logger.info(msg)


# - Transform fact
class TransformFactFromUsingFactTask(object):

    logger = logger

    eventtypes = []

    def get_queryset(self):
        return UsinglogFact.objects.order_by('created_datetime')

    def filter_events(self, queryset, eventtypes):
        if not eventtypes:
            return queryset
        return queryset.filter(event__eventtype__in=eventtypes)

    def filter_between(self, queryset, start_date, end_date):
        datedims = DateDim.objects.between(start_date, end_date)
        return queryset.in_days(datedims)

    def filter_between_datetime(self, queryset, start_date, end_date):
        tz = get_default_timezone()
        s_date = make_aware(start_date, tz) if not is_aware(start_date) else start_date
        e_date = make_aware(end_date, tz) if not is_aware(end_date) else end_date
        return queryset.filter(created_datetime__gte=s_date,
                               created_datetime__lt=e_date)

    def process_between_datetime(self, start_date, end_date):
        queryset = self.get_queryset()
        queryset = self.filter_between_datetime(queryset, start_date, end_date)
        queryset = self.filter_events(queryset=queryset,
                                      eventtypes=self.eventtypes)
        self.extract_to_fact(queryset)

    def process_between(self, start_date, end_date):
        queryset = self.get_queryset()
        queryset = self.filter_between(queryset, start_date, end_date)
        queryset = self.filter_events(queryset=queryset,
                                      eventtypes=self.eventtypes)
        self.extract_to_fact(queryset)

    def extract_to_fact(self, queryset):
        raise NotImplementedError()


class TransformDownloadFactFromUsinglogFactTask(TransformFactFromUsingFactTask):

    eventtypes = ('download', 'downloaded')

    def extract_to_fact(self, queryset):
        cnt = 0
        for usinglog in queryset:
            cnt += 1
            try:
                sid = transaction.savepoint(USING)
                fact = DownloadFact.objects.create_by_usinglogfact(usinglog)
                self.logger.info(",, ".join([
                                             str(fact.event),
                                             str(fact.device_platform),
                                             str(fact.productkey),
                                             str(fact.packagekey),
                                             str(fact.package),
                                             str(fact.download_package),
                                             str(fact.download_packagekey),
                                             str(fact.created_datetime)])
                )
                transaction.savepoint_commit(sid, USING)
            except IntegrityError as e:
                self.logger.warning(e)
                transaction.savepoint_rollback(sid, USING)
                pass
            except PackageDim.DoesNotExist:
                doc = usinglog.doc._data
                self.logger.error(usinglog.pk, usinglog.doc)
                self.logger.error(doc.get('download_package_name'),
                                  doc.get('download_version_name'))
                break
            self.logger.info(cnt)


class TransformActivateFactFromUsinglogFactTask(TransformFactFromUsingFactTask):

    eventtypes = ('open', 'activate')

    def extract_to_fact(self, queryset):
        model = ActivateNewReserveFact
        for usinglog in queryset:
            try:
                sid = transaction.savepoint(USING)
                fact = model.objects.create_by_usinglogfact(usinglog)
                transaction.savepoint_commit(sid, USING)
                self.logger.info(", ".join([
                      str(fact.usinglog.pk),
                      str(fact.created_datetime),
                      str(fact.is_new_product),
                      str(fact.is_new_product_channel),
                      str(fact.is_new_product_package),
                      str(fact.is_new_product_package_version),
                      str(fact.is_new_package),
                      str(fact.is_new_package_version),

                      str(fact.is_new_product_channel_package),
                      str(fact.is_new_product_channel_package_version),
                      ]))
            except IntegrityError as e:
                self.logger.warning(e)
                transaction.savepoint_rollback(sid, USING)


class TransformOpenCloseDailyFactFromUsinglogFactTask(TransformFactFromUsingFactTask):

    eventtypes = ('close', )

    def extract_to_fact(self, queryset):
        for usinglog in queryset:
            try:
                sid = transaction.savepoint(USING)
                start = UsinglogFact.objects.find_open_event_by(usinglog)
                fact = OpenCloseDailyFact.objects.create_by_usinglogfact(start, usinglog)
                transaction.savepoint_commit(sid, USING)
                self.logger.info(fact.start_usinglog.pk, fact.end_usinglog.pk, fact.segment.name)
            except (IntegrityError, UsinglogFact.DoesNotExist) as e:
                self.logger.warning(e)
                transaction.savepoint_rollback(sid, USING)


# - Load result
from datetime import date
_datedims_mapset = dict()


def _fetch_cache_datedims(key, datedims):
    global _datedims_mapset
    if key not in _datedims_mapset:
        _datedims_mapset[key] = list(datedims)
    return _datedims_mapset[key]


CYCLE_TYPES = dict(BaseResult.CYCLE_TYPES)

CHOICE_CYCLE_TYPE = dict(zip(CYCLE_TYPES.values(), CYCLE_TYPES.keys()))


class LoadResultTask(object):

    logger = logger

    CHOICE_CYCLE_TYPE = CHOICE_CYCLE_TYPE

    def __init__(self):
        self.first_datedim = DateDim.objects.get(datevalue=date(2013, 12, 19))

    def get_queryset(self):
        pass

    def filter_between(self, queryset, start_date, end_date):
        return queryset.filter(created_datetime__gte=start_date,
                               created_datetime__lt=end_date)

    def _process_queryset(self, queryset, start_datedim, end_datedim,
                          cycle_type=CHOICE_CYCLE_TYPE['custom']):
        raise NotImplementedError()

    def process_between(self, start_date, end_date,
                        cycle_type=CHOICE_CYCLE_TYPE['custom']):
        if start_date > end_date:
            raise ValueError('end datetime must great than or equal to start datetime')

        start_datedim = DateDim.objects.get(datevalue=start_date.date())
        end_datedim = DateDim.objects.get(datevalue=end_date.date())
        qs = self.filter_between(self.get_queryset(), start_datedim, end_datedim)
        self._process_queryset(queryset=qs,
                               start_datedim=start_datedim,
                               end_datedim=end_datedim,
                               cycle_type=cycle_type)

    def process_daily(self, dt):
        datedims = DateDim.objects.get_daily_dims(dt)
        _datedims = _fetch_cache_datedims(dt.strftime('daily-%Y-%m-%d'), datedims)
        start_datedim = end_datedim = _datedims[0]

        queryset = self.get_queryset().in_days(datedims)
        self._process_queryset(queryset=queryset,
                               start_datedim=start_datedim,
                               end_datedim=end_datedim,
                               cycle_type=self.CHOICE_CYCLE_TYPE['daily'])

    def process_weekly(self, dt):
        days = 7
        dayofweek = int(dt.strftime('%w'))
        if dayofweek != 1:
            return None

        datedims = DateDim.objects.get_weekly_dims(dt)
        _datedims = _fetch_cache_datedims(dt.strftime('weekly-%Y-%W'), datedims)
        start_datedim = _datedims[0]
        end_datedim = _datedims[-1]

        queryset = self.get_queryset().in_days(datedims)
        self._process_queryset(queryset=queryset,
                               start_datedim=start_datedim,
                               end_datedim=end_datedim,
                               cycle_type=self.CHOICE_CYCLE_TYPE['weekly'])

    def process_monthly(self, dt):
        days = 30
        dayofmonth = dt.day
        if dayofmonth != 1:
            return None

        datedims = DateDim.objects.get_monthly_dims(dt)
        _datedims = _fetch_cache_datedims(dt.strftime('monthly-%Y-%m'), datedims)
        start_datedim = _datedims[0]
        end_datedim = _datedims[-1]

        queryset = self.get_queryset().in_days(datedims)
        self._process_queryset(queryset=queryset,
                               start_datedim=start_datedim,
                               end_datedim=end_datedim,
                               cycle_type=self.CHOICE_CYCLE_TYPE['monthly'])

    def process_weekly_by_natural(self, dt):
        dt = dt + relativedelta(weekday=MO(-1))
        self.process_weekly(dt)

    def process_monthly_by_natural(self, dt):
        dt = datetime(dt.year, dt.month, 1)
        self.process_monthly(dt)


class BaseLoadActivateDeviceResultTask(LoadResultTask):

    CHOICE_CYCLE_TYPE = CHOICE_CYCLE_TYPE

    model = None

    sum_field_names = None

    flag_field_name = None

    def get_queryset(self):
        return ActivateNewReserveFact.objects

    def _process_queryset(self, queryset, start_datedim, end_datedim,
                          cycle_type=CHOICE_CYCLE_TYPE['custom']):
        reserve_values = queryset.reserve_device_values(*self.sum_field_names,
                                                        **{self.flag_field_name:True}
        )
        active_values = queryset.active_device_values(*self.sum_field_names)
        open_values = queryset.open_values(*self.sum_field_names)

        total_vals = self._total_activate_values('reserve_count',
                                                 reserve_values)
        self.logger.info(total_vals)
        total_vals = self._total_activate_values('active_count',
                                                 active_values, total_vals)
        self.logger.info(total_vals)
        total_vals = self._total_activate_values('open_count',
                                                 open_values, total_vals)
        self.logger.info(total_vals)

        until_date_reserve_values = self._until_date_total_reserve_values(end_datedim)
        total_vals = self._total_activate_values('total_reserve_count',
                                                 until_date_reserve_values,
                                                 total_vals)
        self.logger.info(total_vals)

        try:
            sid = transaction.savepoint(USING)
            self._save_activate_values(total_vals, cycle_type,
                                       start_datedim, end_datedim)
        except Exception as e:
            self.logger.info(e)
            transaction.savepoint_rollback(sid)

    def _until_date_total_reserve_values(self, end_datedim):
        datedims = DateDim.objects.until_dim(end_datedim, with_self=True)
        values = self.get_queryset() \
            .in_days(datedims) \
            .reserve_device_values(*self.sum_field_names,
                                   **{self.flag_field_name: True} )
        return values

    def _total_activate_values(self, count_field, values, total_vals=None):
        if total_vals is None:
            total_vals = dict()
        for val in values:
            key = tuple({field_name:val[field_name] for field_name in self.sum_field_names}.items())
            if key not in total_vals:
                total_vals[key] = dict()

            total_vals[key][count_field] = \
                total_vals[key].get(count_field, 0) + val['cnt']
        return total_vals

    def _save_activate_values(self, values, cycle_type, start_date, end_date):
        self.logger.info("%s, %s, %s" %(cycle_type, start_date, end_date))

        for key, val in values.items():
            defaults = val
            self.logger.info(key)
            lookup_dict = {"%s_id"%field_name: field_val for field_name, field_val in key}
            lookup_dict.update(cycle_type=cycle_type,
                               start_date=start_date,
                               end_date=end_date)
            self.logger.info(lookup_dict)
            try:
                result, created = self.model.objects.get(**lookup_dict), False
            except self.model.DoesNotExist:
                create_params = deepcopy(lookup_dict)
                create_params.update(**defaults)
                result, created = self.model(**create_params), True
                try:
                    sid = transaction.savepoint(USING)
                    result.save()
                    transaction.savepoint_commit(sid, USING)
                except IntegrityError:
                    transaction.savepoint_rollback(sid, USING)
                    continue

            self.logger.info("created: %s, %s, %s" % (created, lookup_dict, defaults))
            if created:
                continue
                # overwrite count field
            for fieldname in self.model._meta.get_all_field_names():
                if fieldname in defaults:
                    setattr(result, fieldname, defaults.get(fieldname))
                elif fieldname.endswith('_count'):
                    setattr(result, fieldname, 0)
            result.save()


def factory_load_sum_activate_result_task(sum_activate_result_model):
    """
        sum_field_names:
            1.device_paltform, productkey
            2.device_paltform, product(entrytype, channel)
            3.device_paltform, productkey, packagekey
            4.device_paltform, productkey, package(package_name, version_name)
            5.device_paltform, product(entrytype, channel), packagekey
            6.device_paltform, product(entrytype, channel), package(package_name, version_name)

        flag_field_name:
            1. is_new_product
            2. is_new_product_channel
            3. is_new_product_package
            4. is_new_product_package_version
            5. is_new_product_channel_package
            6. is_new_product_channel_package_version

        sum_activate_result_model:

    """
    sum_field_names = sum_activate_result_model._sum_field_names
    flag_field_name = sum_activate_result_model._flag_field_name

    base_name = "".join([name.capitalize() \
                         for name in flag_field_name.lstrip('is_new_').split('_')])
    class_name = 'LoadSumActivateDevice%ssResultTask' % base_name
    class_attrs = {
        'model' : sum_activate_result_model,
        'flag_field_name': flag_field_name,
        'sum_field_names': sum_field_names,
        '__module__': 'analysis.etl'
    }
    return type(BaseLoadActivateDeviceResultTask)(class_name, (BaseLoadActivateDeviceResultTask, ), class_attrs)


LoadSumActivateDeviceProductsResultTask = factory_load_sum_activate_result_task(SumActivateDeviceProductResult)
LoadSumActivateDeviceProductPackagesResultTask = factory_load_sum_activate_result_task(SumActivateDeviceProductPackageResult)
LoadSumActivateDeviceProductPackageVersionsResultTask = factory_load_sum_activate_result_task(SumActivateDeviceProductPackageVersionResult)

LoadSumActivateDeviceProductChannelsResultTask = factory_load_sum_activate_result_task(SumActivateDeviceProductChannelResult)
LoadSumActivateDeviceProductChannelPackagesResultTask = factory_load_sum_activate_result_task(SumActivateDeviceProductChannelPackageResult)
LoadSumActivateDeviceProductChannelPackageVersionsResultTask = factory_load_sum_activate_result_task(SumActivateDeviceProductChannelPackageVersionResult)


def factory_load_cube_activate_result_task(cube_activate_result_model):
    """
        sum_field_names:
            5.device_paltform, product(entrytype, channel), packagekey
            6.device_paltform, product(entrytype, channel), package(package_name, version_name)

        flag_field_name:
            5. is_new_product_channel_package
            6. is_new_product_channel_package_version

        cube_activate_result_model:
    """
    sum_field_names = cube_activate_result_model._sum_field_names
    flag_field_name = cube_activate_result_model._flag_field_name
    base_name = "".join([name.capitalize() \
                         for name in flag_field_name.lstrip('is_new_').split('_')])
    class_name = 'LoadCubeActivateDevice%sResultTask' % base_name
    class_attrs = {
        'model': cube_activate_result_model,
        'flag_field_name': flag_field_name,
        'sum_field_names': sum_field_names,
        '__module__': 'analysis.etl'
    }
    return type(BaseLoadActivateDeviceResultTask)(class_name, (BaseLoadActivateDeviceResultTask, ), class_attrs)


LoadCubeActivateDeviceProductChannelPackageResultTask = factory_load_cube_activate_result_task(CubeActivateDeviceProductChannelPackageResult)
LoadCubeActivateDeviceProductChannelPackageVersionResultTask = factory_load_cube_activate_result_task(CubeActivateDeviceProductChannelPackageVersionResult)


class LoadSumDownloadProductResultTask(LoadResultTask):

    model = SumDownloadProductResult

    def get_queryset(self):
        return DownloadFact.objects

    def _get_download_events(self):
        if not hasattr(self, '_events'):
            eventtypes = ['download', 'downloaded']
            events = dict()
            for e in EventDim.objects.filter(eventtype__in=eventtypes):
                events[e.pk] = e
            self._events = events
        return self._events

    def _process_queryset(self, queryset, start_datedim, end_datedim,
                          cycle_type=CHOICE_CYCLE_TYPE['custom']):
        download_values = queryset.download_values('productkey')
        self.logger.info("%s, %s" %(start_datedim, end_datedim))
        total_download_values = self._until_date_download_values(end_datedim)
        self.logger.info(total_download_values)
        cb_dw_values = self._combine_values(download_values,
                                            result=dict(), is_total=False)
        cb_dw_values = self._combine_values(total_download_values,
                                            cb_dw_values, is_total=True)
        self.logger.info(cb_dw_values)

        try:
            sid = transaction.savepoint(USING)
            self._save_values(cb_dw_values, cycle_type, start_datedim, end_datedim)
            transaction.savepoint_commit(sid)
        except Exception as e:
            self.logger.info(e)
            transaction.savepoint_rollback(sid)

    def _until_date_download_values(self, end_datedim):
        datedims = DateDim.objects.until_dim(end_datedim, with_self=True)
        self.logger.info(datedims.count())
        return self.get_queryset().in_days(datedims).download_values('productkey')

    def _combine_values(self, values, result, is_total=False):
        events = self._get_download_events()
        for val in values:
            key = val['productkey']
            event_pk = val['event']
            eventtype = events[event_pk].eventtype
            if key not in result:
                result[key] = dict(download_count=0, total_download_count=0,
                                   downloaded_count=0, total_downloaded_count=0)

            prefix = ''
            if is_total:
                prefix = 'total_'
            if eventtype == 'download':
                result[key]['%sdownload_count' % prefix] = val['cnt']
            elif eventtype == 'downloaded':
                result[key]['%sdownloaded_count' % prefix] = val['cnt']

        return result

    def _save_values(self, values, cycle_type, start_date, end_date):
        self.logger.info(values)
        for key, val in values.items():
            self.logger.info(key)
            self.logger.info(val)
            defaults = val
            result, creatd = self.model.objects.get_or_create(
                productkey_id=key,
                cycle_type=cycle_type,
                start_date=start_date,
                end_date=end_date,
                defaults=defaults
            )
            if creatd:
                continue

            result.total_download_count = defaults.get('total_download_count', 0)
            result.total_downloaded_count = defaults.get('total_downloaded_count', 0)
            result.download_count = defaults.get('download_count', 0)
            result.downloaded_count = defaults.get('downloaded_count', 0)
            result.save()


class BaseLoadCubeDownloadResultTask(LoadResultTask):

    model = None

    sum_field_names = None

    def get_queryset(self):
        return DownloadFact.objects

    def _get_download_events(self):
        if not hasattr(self, '_events'):
            eventtypes = ['download', 'downloaded']
            events = dict()
            for e in EventDim.objects.filter(eventtype__in=eventtypes):
                events[e.pk] = e
            self._events = events
        return self._events

    def _process_queryset(self, queryset, start_datedim, end_datedim,
                          cycle_type=CHOICE_CYCLE_TYPE['custom']):
        download_values = queryset.download_values(*self.sum_field_names)
        self.logger.info("%s, %s" %(start_datedim, end_datedim))
        total_download_values = self._until_date_download_values(end_datedim)
        self.logger.info(total_download_values)
        cb_dw_values = self._combine_values(download_values,
                                            result=dict(), is_total=False)
        cb_dw_values = self._combine_values(total_download_values,
                                            cb_dw_values, is_total=True)
        self.logger.info(cb_dw_values)
        self._save_values(cb_dw_values, cycle_type, start_datedim, end_datedim)

    def _until_date_download_values(self, end_datedim):
        datedims = DateDim.objects.until_dim(end_datedim, with_self=True)
        self.logger.info(datedims.count())
        return self.get_queryset().in_days(datedims).download_values(*self.sum_field_names)

    def _combine_values(self, values, result, is_total=False):
        events = self._get_download_events()
        for val in values:
            key = tuple({field_name:val[field_name] for field_name in self.sum_field_names}.items())
            event_pk = val['event']
            eventtype = events[event_pk].eventtype
            if key not in result:
                result[key] = dict(download_count=0, total_download_count=0,
                                   downloaded_count=0, total_downloaded_count=0)
            prefix = ''
            if is_total:
                prefix = 'total_'
            if eventtype == 'download':
                result[key]['%sdownload_count' % prefix] = val['cnt']
            elif eventtype == 'downloaded':
                result[key]['%sdownloaded_count' % prefix] = val['cnt']

        return result

    def _save_values(self, values, cycle_type, start_date, end_date):
        self.logger.info(values)
        for key, val in values.items():
            self.logger.info("%s,  %s" % (key, val))
            defaults = val
            lookup_dict = {"%s_id"%field_name: field_val for field_name, field_val in key}
            lookup_dict.update(cycle_type=cycle_type,
                               start_date=start_date,
                               end_date=end_date)
            print(lookup_dict)
            try:
                result, created = self.model.objects.get(**lookup_dict), False
            except self.model.DoesNotExist:
                create_params = deepcopy(lookup_dict)
                create_params.update(**defaults)
                result, created = self.model(**create_params), True
                try:
                    sid = transaction.savepoint(USING)
                    result.save()
                    transaction.savepoint_commit(sid, USING)
                except IntegrityError as e:
                    print(e)
                    transaction.savepoint_rollback(sid, USING)
                    continue

            if created:
                continue
            result.total_download_count = defaults.get('total_download_count', 0)
            result.total_downloaded_count = defaults.get('total_downloaded_count', 0)
            result.download_count = defaults.get('download_count', 0)
            result.downloaded_count = defaults.get('downloaded_count', 0)
            result.save()


def factory_load_cube_download_result_task(model_base_name, cube_download_result_model):
    sum_field_names = cube_download_result_model._sum_field_names
    class_name = 'LoadCubeDownload%sResultTask' % model_base_name
    class_attrs = {
        'model': cube_download_result_model,
        'sum_field_names': sum_field_names,
        '__module__': 'analysis.etl'
    }
    return type(BaseLoadCubeDownloadResultTask)(class_name, (BaseLoadCubeDownloadResultTask, ), class_attrs)


LoadCubeDownloadProductResultTask = factory_load_cube_download_result_task('Product', CubeDownloadProductResult)
LoadCubeDownloadProductPackageResultTask = factory_load_cube_download_result_task('ProductPacakge', CubeDownloadProductPackageResult)
LoadCubeDownloadProductPackageVersionResultTask = factory_load_cube_download_result_task('ProductPacakgeVersion', CubeDownloadProductPackageVersionResult)


class InitialDimensionsTask(object):

    def execute(self):
        self.exec_date_dim()
        self.exec_hour_dim()
        self.exec_usinglogsegment_dim()
        self.exec_usingcountsegment_dim()
        self.exec_event_dim()
        self.exec_baidu_push_dim()

    def exec_date_dim(self):
        start_date = datetime(2013, 8, 1)
        end_date = datetime(2020, 8, 1)
        DateDim.objects.get_or_create_dates_between(start_date, end_date)

    def exec_hour_dim(self):
        HourDim.objects.get_or_create_24_hour()

    def exec_usinglogsegment_dim(self):
        cursor = UsinglogSegmentDim.objects \
            .create(name='30 seconds',
                    startsecond=0,
                    endsecond=timedelta(seconds=30).total_seconds())
        cursor = UsinglogSegmentDim.objects\
            .create(name='30 seconds - 1 minute',
                    startsecond=cursor.endsecond,
                    endsecond=timedelta(minutes=1).total_seconds())
        cursor = UsinglogSegmentDim.objects\
            .create(name='1-3 minutes',
                    startsecond=cursor.endsecond,
                    endsecond=timedelta(minutes=3).total_seconds())
        cursor = UsinglogSegmentDim.objects \
            .create(name='3-5 minutes',
                    startsecond=cursor.endsecond,
                    endsecond=timedelta(minutes=5).total_seconds())
        cursor = UsinglogSegmentDim.objects \
            .create(name='5-10 minutes',
                    startsecond=cursor.endsecond,
                    endsecond=timedelta(minutes=10).total_seconds())
        cursor = UsinglogSegmentDim.objects \
            .create(name='10-30 minutes',
                    startsecond=cursor.endsecond,
                    endsecond=timedelta(minutes=30).total_seconds())
        cursor = UsinglogSegmentDim.objects \
            .create(name='30-60 minutes',
                    startsecond=cursor.endsecond,
                    endsecond=timedelta(hours=1).total_seconds())
        cursor = UsinglogSegmentDim.objects \
            .create(name='1-3 hours',
                    startsecond=cursor.endsecond,
                    endsecond=timedelta(hours=3).total_seconds())
        cursor = UsinglogSegmentDim.objects \
            .create(name='3 hours more',
                    startsecond=cursor.endsecond,
                    endsecond=timedelta(hours=24).total_seconds())

    def exec_usingcountsegment_dim(self):
        cursor = UsingcountSegmentDim.objects \
            .create(name='10 times',
                    startcount=0,
                    endcount=10)
        cursor = UsingcountSegmentDim.objects \
            .create(name='10 - 30 times',
                    startcount=cursor.endcount,
                    endcount=30)
        cursor = UsingcountSegmentDim.objects \
            .create(name='30 - 50 times',
                    startcount=cursor.endcount,
                    endcount=50)
        cursor = UsingcountSegmentDim.objects \
            .create(name='50 - 100 times',
                    startcount=cursor.endcount,
                    endcount=100)
        cursor = UsingcountSegmentDim.objects \
            .create(name='100 - 300 times',
                    startcount=cursor.endcount,
                    endcount=200)
        cursor = UsingcountSegmentDim.objects \
            .create(name='300 - 500 times',
                    startcount=cursor.endcount,
                    endcount=500)
        cursor = UsingcountSegmentDim.objects \
            .create(name='500 - 1000 times',
                    startcount=cursor.endcount,
                    endcount=1000)
        cursor = UsingcountSegmentDim.objects \
            .create(name='more than 1000 times',
                    startcount=cursor.endcount,
                    endcount=100000)

    def exec_event_dim(self):
        EventDim.objects.get_or_create_events()

    def exec_baidu_push_dim(self):
        BaiduPushDim.objects.get_or_create(channel_id=UNDEFINED,
                                    user_id=UNDEFINED,
                                    app_id=UNDEFINED)

    def import_cell_tower_from_csv(self, f):
        from django.utils.timezone import datetime, utc
        from analysis.documents.event import CellTower
        import csv
        reader = csv.reader(f)
        for row in reader:
            try:
                lng=float(row[4])
                lat=float(row[5])
            except ValueError as e:
                print(row[4])
                print(row[5])
                raise e
            samples = int(row[6])
            changeable = True if row[7] == 'true' else False
            created = datetime.fromtimestamp(int(row[8])/1000, utc)
            updated = datetime.fromtimestamp(int(row[9])/1000, utc)
            averageSignalStrength=float(row[10])

            ct = CellTower(
                mcc=int(row[0]),
                mnc=int(row[1]),
                lac=int(row[2]),
                cid=int(row[3]),
                lng=lng,
                lat=lat,
                point=[lng, lat],
                samples=samples,
                changeable=changeable,
                created=created,
                updated=updated,
                averageSignalStrength=averageSignalStrength)
            ct.save()


class ExtractDimensionProcessor(ETLProcessor):

    # Transform Fact
    def transform_to_fact(self, queryset):
        pass


class CleaningPackageDimensionsTask(object):

    def execute(self):
        from django.db.models.query import Q as DQ
        qs = PackageDim.objects.filter(DQ(platform=UNDEFINED,
                                          platform=PLATFORM_ANDROID)) \
            .order_by('package_name', 'version_name')
        for pd in qs:
            try:
                pd.platform = PLATFORM_ANDROID
                pd.save()
            except IntegrityError:
                pd.delete()

        qs = PackageDim.objects.exclude(platform=UNDEFINED)\
            .filter(DQ(pid=None)|DQ(title=''))
        for pd in qs:
            if pd.pid and pd.title:
                continue
            pd = packagecategorydim_fill_to(pd)
            pd = packageversion_id_fill(pd)
            pd.save()
            pkd, created = PackageKeyDim.objects\
                .get_or_create_from_package_dim(pd)



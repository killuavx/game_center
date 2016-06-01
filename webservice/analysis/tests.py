"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.db.models import Count

from django.test import TestCase
from django.utils.timezone import datetime, timedelta, get_default_timezone
from should_dsl import should, should_not
from django.db.utils import IntegrityError
from .models import DateDim, PackageDim, ProductDim, DeviceDim, EventDim, PageDim
from warehouse.models import PackageVersion, Package

warehouse_fixtures = [
    'webservice-20140312-warehouse-taxonomy',
    ]

class DateDimTest(TestCase):

    def test_basic_create(self):
        start_date = DateDim(datevalue=datetime(2014,3,10))
        next_date, created = start_date.get_or_create_next_date()
        next_date.datevalue - start_date.datevalue |should| equal_to(timedelta(days=1))

    def test_create_between(self):
        start = datetime(2014, 3, 10)
        end = datetime(2014, 3, 20)
        result = DateDim.get_or_create_dates_between(start, end)
        result[0][0].datevalue.date() |should| equal_to(start.date())
        result[-1][0].datevalue.date() |should| equal_to(end.date())
        result |should| have(11).elements


class PackageDimTest(TestCase):

    fixtures = [
        'webservice-tiny-warehouse-taxonomy'
    ]

    def test_basic_create(self):
        pd = PackageDim()
        pkg = Package.objects.published().all()[0]
        pd.package = pkg
        pd.package_name = pkg.package_name
        pd.title = pkg.title
        version = pkg.versions.latest_published()
        pd.version = version
        pd.version_name = version.version_name
        pd.save()

        pd.package_name |should| equal_to(pkg.package_name)
        pd.version_name |should| equal_to(version.version_name)
        pd.title |should| equal_to(pkg.title)

    def test_create_by_packageversion(self):
        pd = PackageDim()
        pd.version = PackageVersion.objects.all()[0]
        pd.save()

        pd.package_name |should| equal_to('com.glu.deerhunt2')
        pd.package.package_name |should| equal_to(pd.package_name)
        pd.version_name |should| equal_to('1.1.0')
        pd.version.version_name |should| equal_to(pd.version_name)

    def test_create_by_package_and_versionname(self):
        pd = PackageDim()
        pd.package = Package.objects.all()[0]
        pd.version_name = '1.1.0'
        pd.save()

        pd.title |should_not| be_empty
        pd.package_name |should| equal_to('com.glu.deerhunt2')
        pd.package.package_name |should| equal_to(pd.package_name)
        pd.version_name |should| equal_to('1.1.0')
        pd.version.version_name |should| equal_to(pd.version_name)

    def test_create_by_packagename_versionname(self):
        pd = PackageDim()
        pd.package_name = 'com.glu.deerhunt2'
        pd.version_name = '1.1.0'
        pd.save()

        pd.title |should_not| be_empty
        pd.package_name |should| equal_to('com.glu.deerhunt2')
        pd.package.package_name |should| equal_to(pd.package_name)
        pd.version_name |should| equal_to('1.1.0')
        pd.version.version_name |should| equal_to(pd.version_name)


class ProductDimTest(TestCase):

    def test_basic_create(self):
        prddim = ProductDim()
        prddim.platform = 'android'
        prddim.entrytype = 'game'
        prddim.save()

        expect = ProductDim.objects.get(pk=prddim.pk)
        expect.platform |should| equal_to(1)
        expect.entrytype |should| equal_to('game')
        expect.channel |should| equal_to('')


class DeviceDimTest(TestCase):

    def test_basic_create(self):
        imei = '12345678901234567890'
        dd = DeviceDim(imei=imei)
        dd.platform = 1
        dd.save()
        expect = DeviceDim.objects.get(imei=imei)

        expect.imei |should| equal_to(imei)

        duplication_dd = DeviceDim(imei=imei)
        duplication_dd.save |should| throw(IntegrityError,
                                           'column imei is not unique')


class PageDimTest(TestCase):

    def test_basic_create(self):
        url = 'http://gc.ccplay.com.cn/download/packageversion/493?entrytype=client'
        page = PageDim()
        page.page_url = url
        page.save()

        page.host |should| equal_to('http://gc.ccplay.com.cn')
        page.path |should| equal_to('/download/packageversion/493')
        page.query |should| equal_to('entrytype=client')
        page.page_name |should| be_empty


from .etl import UsinglogETLProcessor

class UsinglogETLProcessorTest(TestCase):

    #fixtures = warehouse_fixtures

    def create_device_dim(self, imei=None):
        if imei:
            imei='0' * 20
        obj, created = DeviceDim.objects.get_or_create(imei=imei)
        return obj

    def create_package_dim(self):
        package = Package.objects.published().all()[0]
        version = package.versions.latest_published()
        pd, created = PackageDim.objects\
            .get_or_create(package=package,
                           version=version,
                           package_name=package.package_name,
                           version_name=version.version_name,
                           title=package.title)
        return pd

    def create_product_dim(self):
        obj, created = ProductDim.objects.create(platform=1, )
        return obj

    def create_date_dim(self, datevalue=None):
        if not datevalue:
            datevalue = datetime.now().replace(hour=0, minute=0,
                                               second=0, microsecond=0)
        obj, created = DateDim.objects.get_or_create(datevalue=datevalue)
        return obj

    def create_event(self, eventtype='open'):
        obj, created = EventDim.objects.get_or_create(eventtype=eventtype)
        return obj

    def test_basic_create(self):
        processor = UsinglogETLProcessor()
        start_date = datetime(2014, 3, 20)
        end_date = datetime(2014, 3, 21)
        processor.process_between(start_date, end_date)


from analysis.etl import *


class MockTaskMixin(object):

    results = list()

    def trans_to_db(self, iterator):
        for doc in iterator:
            kwvals = dict(doc.value)
            if '_id' in kwvals:
                del kwvals['_id']
            kwvals = dict(map(lambda v: (v[0], UNDEFINED) if v[1] is None else v, kwvals.items()))
            self.results.append(kwvals)
            self.dimension_class.objects.get_or_create(defaults=kwvals, **kwvals)


class ExtractQuerySetMixin(object):

    def _get_queryset(self):
        return Event.objects \
            .filter(created_datetime__gte=datetime(2014, 4, 2, tzinfo=get_default_timezone())) \
            .filter(created_datetime__lt=datetime(2014, 4, 3, tzinfo=get_default_timezone())) \
            .filter(imei='A0000042FCEBEA')

    def get_queryset(self):
        return Event.objects \
            .filter(created_datetime__gte=datetime(2014, 4, 4, tzinfo=get_default_timezone())) \
            .filter(created_datetime__lt=datetime(2014, 4, 5, tzinfo=get_default_timezone())) \
            .filter(imei='358403031062411')


class ExtractProductDimensionTaskTest(ExtractQuerySetMixin, TestCase):

    class MockTask(MockTaskMixin, ExtractProductDimensionTask):
        pass

    def test_load(self):
        queryset = self.get_queryset()
        queryset.count() |should| equal_to(542)
        task = self.MockTask(queryset=queryset)
        task.execute()
        for kwargs in task.results:
            (lambda: ProductDim.objects.get(**kwargs)) |should_not| throw(ProductDim.DoesNotExist)


class ExtractPackageDimensionTaskTest(ExtractQuerySetMixin, TestCase):

    class MockTask(MockTaskMixin, ExtractPackageDimensionTask):
        pass

    def test_load(self):
        queryset = self.get_queryset()
        task = self.MockTask(queryset=queryset)
        task.execute()
        for kwargs in task.results:
            (lambda: PackageDim.objects.get(**kwargs)) |should_not| throw(PackageDim.DoesNotExist)


class ExtractSubscriberIdDimensionTaskTest(ExtractQuerySetMixin, TestCase):

    class MockTask(MockTaskMixin, ExtractSubscriberIdDimensionTask):
        pass

    def test_load(self):
        queryset = self.get_queryset()
        task = self.MockTask(queryset=queryset)
        task.execute()
        for kwargs in task.results:
            (lambda: SubscriberIdDim.objects.get(**kwargs)) |should_not| throw(SubscriberIdDim.DoesNotExist)


class ExtractDeviceDimensionTaskTest(ExtractQuerySetMixin, TestCase):

    class MockTask(MockTaskMixin, ExtractDeviceDimensionTask):
        pass

    def test_load(self):
        queryset = self.get_queryset()
        task = self.MockTask(queryset=queryset)
        task.execute()
        for kwargs in task.results:
            (lambda: DeviceDim.objects.get(**kwargs)) |should_not| throw(DeviceDim.DoesNotExist)


class ExtractDevicePlatformDimensionTaskTest(ExtractQuerySetMixin, TestCase):

    class MockTask(MockTaskMixin, ExtractDevicePlatformDimensionTask):
        pass

    def test_load(self):
        queryset = self.get_queryset()
        task = self.MockTask(queryset=queryset)
        task.execute()
        for kwargs in task.results:
            (lambda: DevicePlatformDim.objects.get(**kwargs)) |should_not| throw(DevicePlatformDim.DoesNotExist)


class ExtractDeviceOSDimensionTaskTest(ExtractQuerySetMixin, TestCase):

    class MockTask(MockTaskMixin, ExtractDeviceOSDimensionTask):
        pass

    def test_load(self):
        queryset = self.get_queryset()
        task = self.MockTask(queryset=queryset)
        task.execute()
        for kwargs in task.results:
            (lambda: DeviceOSDim.objects.get(**kwargs)) |should_not| throw(DeviceOSDim.DoesNotExist)


class ExtractDeviceResolutionDimensionTaskTest(ExtractQuerySetMixin, TestCase):

    def get_queryset(self):
        return Event.objects \
            .filter(created_datetime__gte=datetime(2014, 4, 4, tzinfo=get_default_timezone())) \
            .filter(created_datetime__lt=datetime(2014, 4, 5, tzinfo=get_default_timezone()))

    class MockTask(MockTaskMixin, ExtractDeviceResolutionDimensionTask):

        results = []

        def trans_to_db(self, iterator):
            for doc in iterator:
                orig_resolution = dict(doc.value).get('resolution') or UNDEFINED
                inst, created = self.dimension_class.objects\
                    .get_or_create_by_orig_resolution(orig_resolution)
                self.results.append(inst)

    def test_load_with_invalid_resolution(self):
        queryset = self.get_queryset().limit(5)
        task = self.MockTask(queryset=queryset)
        task.execute()
        for inst in task.results:
            inst.pk |should_not| be(None)

    def test_load(self):
        queryset = self.get_queryset().filter(resolution__exists=True).limit(50)
        task = self.MockTask(queryset=queryset)
        task.execute()
        for inst in task.results:
            inst.pk |should_not| be(None)


class ExtractDeviceModelDimensionTaskTest(ExtractQuerySetMixin, TestCase):

    class MockTask(MockTaskMixin, ExtractDeviceModelDimensionTask):
        pass

    def test_load(self):
        queryset = self.get_queryset()
        task = self.MockTask(queryset=queryset)
        task.execute()
        for kwargs in task.results:
            (lambda: DeviceModelDim.objects.get(**kwargs)) |should_not| throw(DeviceModelDim.DoesNotExist)


class ExtractDeviceSupplierDimensionTaskTest(ExtractQuerySetMixin, TestCase):

    class MockTask(MockTaskMixin, ExtractDeviceSupplierDimensionTask):
        pass

    def test_load(self):
        queryset = self.get_queryset()
        task = self.MockTask(queryset=queryset)
        task.execute()
        for kwargs in task.results:
            (lambda: DeviceSupplierDim.objects.get(**kwargs)) |should_not| throw(DeviceSupplierDim.DoesNotExist)


class ExtractDeviceLanguageDimensionTaskTest(ExtractQuerySetMixin, TestCase):

    class MockTask(MockTaskMixin, ExtractDeviceLanguageDimensionTask):
        pass

    def test_load(self):
        queryset = self.get_queryset()
        task = self.MockTask(queryset=queryset)
        task.execute()
        for kwargs in task.results:
            (lambda: DeviceLanguageDim.objects.get(**kwargs)) |should_not| throw(DeviceLanguageDim.DoesNotExist)


class ExtractDeviceNetworkDimensionTaskTest(ExtractQuerySetMixin, TestCase):

    class MockTask(MockTaskMixin, ExtractNetworkDimensionTask):
        pass

    def test_load(self):
        queryset = self.get_queryset()
        task = self.MockTask(queryset=queryset)
        task.execute()
        for kwargs in task.results:
            (lambda: NetworkDim.objects.get(**kwargs)) |should_not| throw(NetworkDim.DoesNotExist)


class ExtractPageDimensionTaskTest(ExtractQuerySetMixin, TestCase):

    class MockTask(MockTaskMixin, ExtractPageDimensionTask):
        pass

    def test_load(self):
        queryset = self.get_queryset()
        task = self.MockTask(queryset=queryset)
        task.execute()
        for kwargs in task.results:
            (lambda: PageDim.objects.get(**kwargs)) |should_not| throw(PageDim.DoesNotExist)


class ExtractBaiduPushDimensionTaskTest(ExtractQuerySetMixin, TestCase):

    class MockTask(MockTaskMixin, ExtractBaiduPushDimensionTask):

        def filter_queryset(self, queryset):
            return queryset

    def get_queryset(self):
        return Event.objects \
            .filter(created_datetime__gte=datetime(2014, 4, 4, tzinfo=get_default_timezone())) \
            .filter(created_datetime__lt=datetime(2014, 4, 5, tzinfo=get_default_timezone()))

    def test_load(self):
        queryset = self.get_queryset()
        task = self.MockTask(queryset=queryset)
        task.execute()
        for kwargs in task.results:
            (lambda: BaiduPushDim.objects.get(**kwargs)) |should_not| throw(BaiduPushDim.DoesNotExist)


class MockETLProcessorMixin(object):

    def get_doc_queryset(self):
        return Event.objects.limit(10)


class MockInitialDimTask(InitialDimensionsTask):

    def exec_date_dim(self):
        start_date = datetime(2014, 4, 1, tzinfo=utc)
        end_date = datetime(2014, 4, 10, tzinfo=utc)
        DateDim.objects.get_or_create_dates_between(start_date, end_date)


class UsinglogETLProcessorTest(TestCase):

    class MockETLProcessor(MockETLProcessorMixin, UsinglogETLProcessor):
        pass

    @classmethod
    def setUpClass(cls):
        task = MockInitialDimTask()
        task.execute()

    def test_processor(self):
        start = datetime(2014, 4, 1, tzinfo=utc)
        end = datetime(2014, 4, 3, tzinfo=utc)
        processor = self.MockETLProcessor()
        processor.process_between(start, end)


def dict_to_model_instance(from_dict, instance):
    for k, v in from_dict.items():
        if not k.startswith('_') and \
                        k != 'id' and k in instance.__dict__:
            instance.__dict__[k] = deepcopy(v)
    return instance


def model_instance_data(instance):
    data = dict()
    for k, v in instance.__dict__.items():
        if k.startswith('_') or k == 'id':
            continue
        data[k] = v
    return data


class TestCaseMixin(object):

    @classmethod
    def setUpClass(self):
        self.usinglog_elt = UsinglogETLProcessor()
        task = MockInitialDimTask()
        task.execute()

    def setUp(self):
        self.model_inst_pools = []

    def tearDown(self):
        self.model_inst_pools.reverse()
        [m.delete() for m in self.model_inst_pools]
        self.model_inst_pools = []

    def extract_dimensions(self, doc):
        data = doc._data
        for extract_class in self.usinglog_elt.extract_classes:
            inst, created = extract_class.get_or_create_dimension(data)
            if created:
                self.model_inst_pools.append(inst)
        d = dict(page_name=data.get('referer'))
        ExtractPageDimensionTask.get_or_create_dimension(d)


class UsinglogFactTest(TestCaseMixin, TestCase):

    @classmethod
    def setUpClass(cls):
        cls.setUpClass()

    def setUp(self):
        self.setUp()

    def tearDown(self):
        self.tearDown()

    def _doc_queryset(self):
        imei = '358403031062411'
        return Event.objects \
            .filter(imei=imei,
                    created_datetime__gte=datetime(2014, 4, 4, tzinfo=utc))

    def test_create_usinglog_activate(self):
        # /* 0 */ open
        # new_device
        # new_device_package
        # new_device_package_version
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4 , 4, 2, 43, 52),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.view.BarLayout",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })
        self.extract_dimensions(doc)
        usinglog = UsinglogFact.objects.create_by_doc(doc)

        usinglog.event.eventtype |should| equal_to('open')
        usinglog.product.entrytype |should| equal_to('game')

        usinglog.device.imei |should| equal_to(doc.imei)
        usinglog.device_resolution.orig_resolution |should| equal_to(doc.resolution)
        usinglog.device_platform.platform |should| equal_to(doc.platform)

        usinglog.device_model.manufacturer |should| equal_to(doc.manufacturer)
        usinglog.device_model.device_name |should| equal_to(doc.device_name)
        usinglog.device_model.module_name |should| equal_to(doc.module_name)
        usinglog.device_model.model_name |should| equal_to(doc.model_name)

        usinglog.network.network |should| equal_to(doc.network)
        usinglog.page.page_name |should| equal_to(doc.page_name)
        usinglog.device_language.language |should| equal_to(doc.language)
        usinglog.subscriberid.imsi |should| equal_to(doc.imsi)
        usinglog.package.package_name |should| equal_to(doc.package_name)
        usinglog.package.version_name |should| equal_to(doc.version_name)
        from django.utils.timezone import localtime

        tzinfo = doc.created_datetime.tzinfo
        doc_created_datetime = localtime(doc.created_datetime.replace(tzinfo=utc))
        usinglog.created_datetime |should| equal_to(doc_created_datetime)

        activate = ActivateFact.objects.create_by_usinglogfact(usinglog)
        activate.is_new_device |should| be(True)
        activate.is_new_device_package |should| be(True)
        activate.is_new_device_package_version |should| be(True)
        self.model_inst_pools.append(doc)
        self.model_inst_pools.append(usinglog)
        self.model_inst_pools.append(activate)

        # not new device/package/version
        doc2 = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk",
            "version_name" : "1.0",
            "created_datetime" : datetime(2014,4,4,2,43,56),
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_gps" : True,
            "resolution" : "540x960",
            "model_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "phone_type" : 1,
            "have_wifi" : True,
            "have_gravity" : True,
            "have_bt" : True,
            "module_name" : "C8815",
            "os_version" : "4.1.2",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "baidu_push_app_id" : "1988517",
            "baidu_push_channel_id" : "4370191336036491262",
            "baidu_push_user_id" : "885069327297809765",
            "device_name" : "HUAWEI C8815",
            "is_mobiledevice" : True,
            "platform" : "android",
            "client_ip" : "180.154.216.154"
        })
        self.extract_dimensions(doc2)
        usinglog2 = UsinglogFact.objects.create_by_doc(doc2)
        activate2 = ActivateFact.objects.create_by_usinglogfact(usinglog2)
        activate2.is_new_device |should| be(False)
        activate2.is_new_device_package |should| be(False)
        activate2.is_new_device_package_version |should| be(False)
        self.model_inst_pools.append(doc2)
        self.model_inst_pools.append(usinglog2)
        self.model_inst_pools.append(activate2)

        # not new device
        # new package/version
        doc3 = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk.anthor.newpackage",
            "version_name" : "1.0.1",
            "created_datetime" : datetime(2014,4,4,2,43,56),
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_gps" : True,
            "resolution" : "540x960",
            "baidu_push_channel_id" : "4370191336036491262",
            "model_name" : "HUAWEI C8815",
            "baidu_push_app_id" : "1988517",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "phone_type" : 1,
            "have_wifi" : True,
            "have_gravity" : True,
            "have_bt" : True,
            "module_name" : "C8815",
            "os_version" : "4.1.2",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "baidu_push_user_id" : "885069327297809765",
            "device_name" : "HUAWEI C8815",
            "is_mobiledevice" : True,
            "platform" : "android",
            "client_ip" : "180.154.216.154"
        })
        self.extract_dimensions(doc3)
        usinglog3 = UsinglogFact.objects.create_by_doc(doc3)
        activate3 = ActivateFact.objects.create_by_usinglogfact(usinglog3)
        activate3.is_new_device |should| be(False)
        activate3.is_new_device_package |should| be(True)
        activate3.is_new_device_package_version |should| be(True)
        self.model_inst_pools.append(doc3)
        self.model_inst_pools.append(usinglog3)
        self.model_inst_pools.append(activate3)

        # /* 4 */
        # not new device
        # not new package/version
        doc4 = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk.anthor.newpackage",
            "version_name" : "1.0.1",
            "created_datetime" : datetime(2014, 4, 4, 2, 44, 44),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.SdkMainActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })
        self.extract_dimensions(doc4)
        usinglog4 = UsinglogFact.objects.create_by_doc(doc4)
        activate4 = ActivateFact.objects.create_by_usinglogfact(usinglog4)
        activate4.is_new_device |should| be(False)
        activate4.is_new_device_package |should| be(False)
        activate4.is_new_device_package_version |should| be(False)
        self.model_inst_pools.append(doc4)
        self.model_inst_pools.append(usinglog4)
        self.model_inst_pools.append(activate4)

        # /* 5 */
        # new device/package/version
        doc5 = Event.objects.create(**{
            "imei" : "958403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "version_name" : "1.0.1",
            "created_datetime" : datetime(2014, 4, 4, 2, 44, 44),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.SdkMainActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })
        self.extract_dimensions(doc5)
        usinglog5 = UsinglogFact.objects.create_by_doc(doc5)
        activate5 = ActivateFact.objects.create_by_usinglogfact(usinglog5)
        activate5.is_new_device |should| be(True)
        activate5.is_new_device_package |should| be(True)
        activate5.is_new_device_package_version |should| be(True)
        self.model_inst_pools.append(doc5)
        self.model_inst_pools.append(usinglog5)
        self.model_inst_pools.append(activate5)

    def tmp(self):
        # /* 2 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "click",
            "tags" : [
                "点击虫"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 44, 44),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.view.BarLayout",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })


        # /* 4 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "close",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 44, 44),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.SdkMainActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })

        # /* 5 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "open",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 44, 44),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.RecommendListActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })

        # /* 6 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "close",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 44, 44),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.RecommendListActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })

        # /* 7 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "open",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 44, 44),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.RecommendDetailActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })

        # /* 8 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "download",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 44, 44),
            "phone_type" : 1,
            "have_wifi" : True,
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154",
            "download_package_name" : "jp.colopl.longfoot",
            "download_version_name" : "1.0.2.0",
            "current_uri" : "http://gc.ccplay.com.cn/download/packageversion/845?entrytype=client",
            "redirect_to" : "http://media.ccplay.com.cn/media/package/830/v4/application.apk"
        })

        # /* 9 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "downloaded",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 44, 44),
            "phone_type" : 1,
            "have_wifi" : True,
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "platform" : "android",
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50001,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "current_uri" : "http://gc.ccplay.com.cn/download/packageversion/845?entrytype=client",
            "client_ip" : "180.154.216.154"
        })

        # /* 10 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "close",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 44, 44),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.RecommendDetailActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50001,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })

        # /* 11 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 45, 45),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.view.BarLayout",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 45411,
                "lac" : 6275,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })

        # /* 12 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "open",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 45, 45),
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_gps" : True,
            "resolution" : "540x960",
            "baidu_push_channel_id" : "4370191336036491262",
            "model_name" : "HUAWEI C8815",
            "baidu_push_app_id" : "1988517",
            "version_name" : "1.0",
            "cell" : {
                "cid" : 45411,
                "lac" : 6275,
                "mcc" : 460,
                "mnc" : 0
            },
            "phone_type" : 1,
            "have_wifi" : True,
            "have_gravity" : True,
            "have_bt" : True,
            "module_name" : "C8815",
            "os_version" : "4.1.2",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "baidu_push_user_id" : "885069327297809765",
            "device_name" : "HUAWEI C8815",
            "is_mobiledevice" : True,
            "platform" : "android",
            "client_ip" : "180.154.216.154"
        })

        # /* 13 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "click",
            "tags" : [
                "点击虫"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 45, 45),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.view.BarLayout",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 45411,
                "lac" : 6275,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })

        # /* 14 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "open",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 45, 45),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.SdkMainActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 45411,
                "lac" : 6275,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })

        # /* 15 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "open",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 45, 45),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.RecommendListActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 45411,
                "lac" : 6275,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })

        # /* 16 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "close",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 45, 45),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.SdkMainActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 45411,
                "lac" : 6275,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })

        # /* 17 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "close",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 46, 46),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.RecommendListActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 45411,
                "lac" : 6275,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })

        # /* 18 */
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "open",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 46, 46),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.RecommendDetailActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 45411,
                "lac" : 6275,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })

        # /* 19 */ close
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "close",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 51, 51),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.RecommendDetailActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 45411,
                "lac" : 6275,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })

    def test_create_activate_device_result(self):
        data = {
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4 , 4, 2, 13, 52),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.view.BarLayout",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        }
        doc = Event.objects.create(**data)
        self.extract_dimensions(doc)
        usinglog = UsinglogFact.objects.create_by_doc(doc)
        self.model_inst_pools.append(doc)
        data.update(eventtype='close',
                    created_datetime=data['created_datetime'] + timedelta(minutes=3))
        doc_close = Event.objects.create(**data)
        usinglog_close = UsinglogFact.objects.create_by_doc(doc_close)
        self.model_inst_pools.append(doc)
        self.model_inst_pools.append(doc_close)
        self.model_inst_pools.append(usinglog)
        self.model_inst_pools.append(usinglog_close)

        data = {
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk.anthor.newpackage",
            "version_name" : "1.0.1",
            "created_datetime" : datetime(2014,4,4,2,43,56),
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_gps" : True,
            "resolution" : "540x960",
            "baidu_push_channel_id" : "4370191336036491262",
            "model_name" : "HUAWEI C8815",
            "baidu_push_app_id" : "1988517",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "phone_type" : 1,
            "have_wifi" : True,
            "have_gravity" : True,
            "have_bt" : True,
            "module_name" : "C8815",
            "os_version" : "4.1.2",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "baidu_push_user_id" : "885069327297809765",
            "device_name" : "HUAWEI C8815",
            "is_mobiledevice" : True,
            "platform" : "android",
            "client_ip" : "180.154.216.154"
        }
        doc3 = Event.objects.create(**data)
        self.extract_dimensions(doc3)
        usinglog3 = UsinglogFact.objects.create_by_doc(doc3)
        data.update(eventtype='close',
                    created_datetime=data['created_datetime'] + timedelta(minutes=3))
        doc3_close = Event.objects.create(**data)
        self.extract_dimensions(doc3_close)
        usinglog3_close = UsinglogFact.objects.create_by_doc(doc3_close)
        self.model_inst_pools.append(doc3)
        self.model_inst_pools.append(doc3_close)
        self.model_inst_pools.append(usinglog3)
        self.model_inst_pools.append(usinglog3_close)


        # /* 5 */
        # new device/package/version
        data = {
            "imei" : "958403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "activate",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "version_name" : "1.0.1",
            "created_datetime" : datetime(2014, 4, 4, 3, 44, 44),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.SdkMainActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        }
        doc5 = Event.objects.create(**data)
        self.extract_dimensions(doc5)
        usinglog5 = UsinglogFact.objects.create_by_doc(doc5)
        data.update(eventtype='close',
                    created_datetime=data['created_datetime'] + timedelta(minutes=3))
        doc5_close = Event.objects.create(**data)
        self.extract_dimensions(doc5_close)
        usinglog5_close = UsinglogFact.objects.create_by_doc(doc5_close)

        self.model_inst_pools.append(doc5)
        self.model_inst_pools.append(doc5_close)
        self.model_inst_pools.append(usinglog5)
        self.model_inst_pools.append(usinglog5_close)


        processor = ExtractActivateFactFromUsinglogFactProcessor()
        start = datetime(2014,4, 1)
        end = datetime(2014, 4, 5)
        processor.process_between(start, end)
        ActivateFact.objects.all().count() |should| equal_to(3)

    def test_create_usinglog_click(self):
        pass

    def test_create_usinglog_openclose(self):
        data = {
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4 , 4, 2, 13, 52),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.view.BarLayout",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        }
        doc = Event.objects.create(**data)
        self.extract_dimensions(doc)
        usinglog = UsinglogFact.objects.create_by_doc(doc)
        self.model_inst_pools.append(doc)
        data.update(eventtype='close',
                    created_datetime=data['created_datetime'] + timedelta(minutes=3))
        doc_close = Event.objects.create(**data)
        usinglog_close = UsinglogFact.objects.create_by_doc(doc_close)
        self.model_inst_pools.append(doc)
        self.model_inst_pools.append(doc_close)
        self.model_inst_pools.append(usinglog)
        self.model_inst_pools.append(usinglog_close)

        # 2 /* 3 */
        data = {
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk.anthor.newpackage",
            "version_name" : "1.0.1",
            "created_datetime" : datetime(2014,4,4,2,43,56),
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_gps" : True,
            "resolution" : "540x960",
            "baidu_push_channel_id" : "4370191336036491262",
            "model_name" : "HUAWEI C8815",
            "baidu_push_app_id" : "1988517",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "phone_type" : 1,
            "have_wifi" : True,
            "have_gravity" : True,
            "have_bt" : True,
            "module_name" : "C8815",
            "os_version" : "4.1.2",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "baidu_push_user_id" : "885069327297809765",
            "device_name" : "HUAWEI C8815",
            "is_mobiledevice" : True,
            "platform" : "android",
            "client_ip" : "180.154.216.154"
        }
        doc3 = Event.objects.create(**data)
        self.extract_dimensions(doc3)
        usinglog3 = UsinglogFact.objects.create_by_doc(doc3)
        data.update(eventtype='close',
                    created_datetime=data['created_datetime'] + timedelta(minutes=3))
        doc3_close = Event.objects.create(**data)
        self.extract_dimensions(doc3_close)
        usinglog3_close = UsinglogFact.objects.create_by_doc(doc3_close)
        self.model_inst_pools.append(doc3)
        self.model_inst_pools.append(doc3_close)
        self.model_inst_pools.append(usinglog3)
        self.model_inst_pools.append(usinglog3_close)


        # 3 /* 5 */
        # new device/package/version
        data = {
            "imei" : "958403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            # ignore eventtype activate
            "eventtype" : "activate",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "version_name" : "1.0.1",
            "created_datetime" : datetime(2014, 4, 4, 3, 44, 44),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.SdkMainActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        }
        doc5 = Event.objects.create(**data)
        self.extract_dimensions(doc5)
        usinglog5 = UsinglogFact.objects.create_by_doc(doc5)
        data.update(eventtype='close',
                    created_datetime=data['created_datetime'] + timedelta(minutes=3))
        doc5_close = Event.objects.create(**data)
        self.extract_dimensions(doc5_close)
        usinglog5_close = UsinglogFact.objects.create_by_doc(doc5_close)

        self.model_inst_pools.append(doc5)
        self.model_inst_pools.append(doc5_close)
        self.model_inst_pools.append(usinglog5)
        self.model_inst_pools.append(usinglog5_close)

        processor = self.MockEAFTask()
        start = datetime(2014, 4, 1)
        end = datetime(2014, 4, 5)
        processor.process_between(start, end)
        ActivateFact.objects.all().count() |should| equal_to(3)
        self.model_inst_pools += processor.result

        ocprocessor = self.MockOCFTask()
        ocprocessor.process_between(start, end)
        self.model_inst_pools += ocprocessor.result

        OpenCloseDailyFact.objects.all().count() |should| equal_to(2)
        ocfacts = list(OpenCloseDailyFact.objects.all())
        ocf1 = ocfacts[0]
        (ocf1.segment.startsecond <= ocf1.duration < ocf1.segment.endsecond) |should| be(True)
        ocf2 = ocfacts[1]
        (ocf2.segment.startsecond <= ocf2.duration < ocf2.segment.endsecond) |should| be(True)

    class MockOCFTask(TransformOpenCloseDailyFactFromUsinglogFactTask):

        result = []

        def extract_to_fact(self, queryset):
            for usinglog in queryset:
                try:
                    start = UsinglogFact.objects.find_open_event_by(usinglog)
                    if start:
                        fact = OpenCloseDailyFact.objects.create_by_usinglogfact(start, usinglog)
                        self.result.append(fact)
                except (IntegrityError, UsinglogFact.DoesNotExist) as e:
                    pass

    class MockEAFTask(TransformActivateFactFromUsinglogFactTask):

        result = []

        def extract_to_fact(self, queryset):
            for usinglog in queryset:
                try:
                    fact = ActivateFact.objects.create_by_usinglogfact(usinglog)
                    self.result.append(fact)
                except IntegrityError:
                    pass

        def load_to_result_between(self, start_date, end_date):
            pass

    def test_create_downloaded_fact(self):
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "download",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014,4,4,2,44,30),
            "phone_type" : 1,
            "have_wifi" : True,
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154",
            "download_package_name" : "jp.colopl.longfoot",
            "download_version_name" : "1.0.2.0",
            "current_uri" : "http://gc.ccplay.com.cn/download/packageversion/845?entrytype=client",
            "redirect_to" : "http://media.ccplay.com.cn/media/package/830/v4/application.apk"
        })

        usinglog_download = UsinglogFact.objects.create_by_doc(doc)
        usinglog_download.event.entrytype |should| equal_to('download')
        download = DownloadFact.objects.create_by_usinglogfact(usinglog_download)
        download.download_package.package_name |should| equal_to()

        doc.delete()

    def test_create_download_fact(self):
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "sdk",
            "eventtype" : "downloaded",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4, 4, 2, 44,57),
            "phone_type" : 1,
            "have_wifi" : True,
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "platform" : "android",
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50001,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "current_uri" : "http://gc.ccplay.com.cn/download/packageversion/845?entrytype=client",
            "client_ip" : "180.154.216.154"
        })

        usinglog = UsinglogFact.objects.create_by_doc(doc)
        usinglog.event.entrytype |should| equal_to('downloaded')

        df = DownloadFact.objects.create_by_usinglogfact(usinglog)
        df.download_package.package_name |should| equal_to()
        df.download_package.version_name |should| equal_to()

        doc.delete()


class ActivateETLProcessorResultTest(TestCaseMixin, TestCase):

    def _fixture_data(self):
        # /* 0 */ open
        # new_device
        # new_device_package
        # new_device_package_version
        doc = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "created_datetime" : datetime(2014, 4 , 4, 2, 43, 52),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.view.BarLayout",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "version_name" : "1.0",
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })
        self.extract_dimensions(doc)
        usinglog = UsinglogFact.objects.create_by_doc(doc)
        activate = ActivateFact.objects.create_by_usinglogfact(usinglog)
        activate.is_new_device |should| be(True)
        activate.is_new_device_package |should| be(True)
        activate.is_new_device_package_version |should| be(True)
        self.model_inst_pools.append(doc)
        self.model_inst_pools.append(usinglog)
        self.model_inst_pools.append(activate)

        # not new device/package/version
        doc2 = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk",
            "version_name" : "1.0",
            "created_datetime" : datetime(2014,4,4,2,43,56),
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_gps" : True,
            "resolution" : "540x960",
            "model_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "phone_type" : 1,
            "have_wifi" : True,
            "have_gravity" : True,
            "have_bt" : True,
            "module_name" : "C8815",
            "os_version" : "4.1.2",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "baidu_push_app_id" : "1988517",
            "baidu_push_channel_id" : "4370191336036491262",
            "baidu_push_user_id" : "885069327297809765",
            "device_name" : "HUAWEI C8815",
            "is_mobiledevice" : True,
            "platform" : "android",
            "client_ip" : "180.154.216.154"
        })
        self.extract_dimensions(doc2)
        usinglog2 = UsinglogFact.objects.create_by_doc(doc2)
        activate2 = ActivateFact.objects.create_by_usinglogfact(usinglog2)
        activate2.is_new_device |should| be(False)
        activate2.is_new_device_package |should| be(False)
        activate2.is_new_device_package_version |should| be(False)
        self.model_inst_pools.append(doc2)
        self.model_inst_pools.append(usinglog2)
        self.model_inst_pools.append(activate2)

        # not new device
        # new package/version
        doc3 = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [],
            "package_name" : "com.lion.lionbarsdk.anthor.newpackage",
            "version_name" : "1.0.1",
            "created_datetime" : datetime(2014,4,4,2,43,56),
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_gps" : True,
            "resolution" : "540x960",
            "baidu_push_channel_id" : "4370191336036491262",
            "model_name" : "HUAWEI C8815",
            "baidu_push_app_id" : "1988517",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "phone_type" : 1,
            "have_wifi" : True,
            "have_gravity" : True,
            "have_bt" : True,
            "module_name" : "C8815",
            "os_version" : "4.1.2",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "baidu_push_user_id" : "885069327297809765",
            "device_name" : "HUAWEI C8815",
            "is_mobiledevice" : True,
            "platform" : "android",
            "client_ip" : "180.154.216.154"
        })
        self.extract_dimensions(doc3)
        usinglog3 = UsinglogFact.objects.create_by_doc(doc3)
        activate3 = ActivateFact.objects.create_by_usinglogfact(usinglog3)
        activate3.is_new_device |should| be(False)
        activate3.is_new_device_package |should| be(True)
        activate3.is_new_device_package_version |should| be(True)
        self.model_inst_pools.append(doc3)
        self.model_inst_pools.append(usinglog3)
        self.model_inst_pools.append(activate3)

        # /* 4 */
        # not new device
        # not new package/version
        doc4 = Event.objects.create(**{
            "imei" : "358403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk.anthor.newpackage",
            "version_name" : "1.0.1",
            "created_datetime" : datetime(2014, 4, 4, 2, 44, 44),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.SdkMainActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })
        self.extract_dimensions(doc4)
        usinglog4 = UsinglogFact.objects.create_by_doc(doc4)
        activate4 = ActivateFact.objects.create_by_usinglogfact(usinglog4)
        activate4.is_new_device |should| be(False)
        activate4.is_new_device_package |should| be(False)
        activate4.is_new_device_package_version |should| be(False)
        self.model_inst_pools.append(doc4)
        self.model_inst_pools.append(usinglog4)
        self.model_inst_pools.append(activate4)

        # /* 5 */
        # new device/package/version
        doc5 = Event.objects.create(**{
            "imei" : "958403031062411",
            "user_pk" : -1,
            "entrytype" : "game",
            "eventtype" : "open",
            "tags" : [
                "LionBarSdk"
            ],
            "package_name" : "com.lion.lionbarsdk",
            "version_name" : "1.0.1",
            "created_datetime" : datetime(2014, 4, 4, 2, 44, 44),
            "phone_type" : 1,
            "have_wifi" : True,
            "page_name" : "com.lion.lionbarsdk.app.SdkMainActivity",
            "imsi" : "460023356827819",
            "wifi_mac" : "08:7a:4c:96:94:0f",
            "network" : "wifi",
            "have_bt" : True,
            "have_gps" : True,
            "resolution" : "540x960",
            "module_name" : "C8815",
            "have_gravity" : True,
            "model_name" : "HUAWEI C8815",
            "platform" : "android",
            "language" : "zh",
            "manufacturer" : "HUAWEI",
            "is_mobiledevice" : True,
            "device_name" : "HUAWEI C8815",
            "cell" : {
                "cid" : 50817,
                "lac" : 6208,
                "mcc" : 460,
                "mnc" : 0
            },
            "os_version" : "4.1.2",
            "client_ip" : "180.154.216.154"
        })
        self.extract_dimensions(doc5)
        usinglog5 = UsinglogFact.objects.create_by_doc(doc5)
        activate5 = ActivateFact.objects.create_by_usinglogfact(usinglog5)
        activate5.is_new_device |should| be(True)
        activate5.is_new_device_package |should| be(True)
        activate5.is_new_device_package_version |should| be(True)
        self.model_inst_pools.append(doc5)
        self.model_inst_pools.append(usinglog5)
        self.model_inst_pools.append(activate5)

    def _create_event(self):
        pass

    def test_activate_processor(self):
        self._fixture_data()

        processor = self.MockLoadResultActiveDevicesTask()
        processor.process_between(datetime(2014, 4, 4), datetime(2014, 4, 5))

        SumTotalReserveDevicesDailyResult.objects.all().count() |should| equal_to(2)
        #SumTotalActiveDevicesDailyResult.objects.all().count() |should| equal_to(2)



from django.test import TestCase
from django.test import LiveServerTestCase


class _SimpleTest(LiveServerTestCase):

    def setUp(self):
        #self.prepare_adv_widget_data()
        pass

    def prepare_adv_widget_data(self):
        from django.utils.timezone import now
        from mezzanine.blog.models import BlogPost
        from promotion.models import Place, Advertisement, Advertisement_Places
        Place.objects.create(slug='home-top-banner')
        place = Place.objects.create(slug='home-top-carousel-adv')
        post = BlogPost.objects.create(title="ttt",
                                       publish_date=now(),
                                       user_id=-1,
                                       content="test content")
        adv = Advertisement.objects.create(title="test",
                                           content=post,
                                           status='published',
                                           released_datetime=now())
        Advertisement_Places.objects.create(place=place, advertisement=adv)

    def test_categories_page_through_ajax(self):
        self.client.get('/categories/big-game',
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')


from should_dsl import should
from django.contrib.sites.models import Site
from website.cdn.core import Feedback
from website.cdn.processors.base import StaticProcessor
from website.cdn.processors.warehouse import PackageVersionProcessor
from website.documents.cdn import SyncQueue
from website.cdn import feedback_signals as fb_signals
from website.cdn.parsers import OperationRequest, FeedbackContextParser


class CDNTestCase(TestCase):

    def setUp(self):
        current_site = Site.objects.get_current()
        current_site.domain = 'gc.ccplay.com.cn'
        current_site.save()

        class MockOperationRequest(OperationRequest):

            def request(self):
                self.request_data = self.create_querydata()
                STATUS_CODE_SUCCESS = self.response_class.STATUS_CODE_SUCCESS
                return self.response_class(STATUS_CODE_SUCCESS, 'receive finish')

        class MockProcessorMixin(object):

            request_class = MockOperationRequest

            def get_source_host(self):
                return 'gc.ccplay.com.cn'

        class MockStaticProcessor(MockProcessorMixin, StaticProcessor):
            pass

        class MockPackageVersionProcessor(MockProcessorMixin, PackageVersionProcessor):
            pass

        self.static_processor_class = MockStaticProcessor
        self.packageversion_processor_class = MockPackageVersionProcessor

        class MockFeedBack(Feedback):
            pass

        self.feedback_class = MockFeedBack

    def tearDown(self):
        SyncQueue.objects.delete()
        pass

    def test_publish_one_static_file(self):
        processor = self.static_processor_class('css/main.css')
        flag, result, faileds = processor.publish()
        flag |should| be(True)
        result |should| have(1).elements
        faileds |should| be_empty

        response, item, queue = result[0]
        item.op_result |should| equal_to('SUCCESS')
        item.op_name |should| equal_to('publish')

        queue = SyncQueue.objects(**{'operations.0.item_id': item.item_id}).get()
        expect_item = queue.operations[0]
        expect_item.item_id |should| equal_to(item.item_id)

    def test_update_one_static_file(self):
        processor = self.static_processor_class('css/main.css')
        flag, result, faileds = processor.publish()
        flag |should| be(True)
        result |should| have(1).elements
        faileds |should| be_empty

        flag, result, faileds = processor.update()
        flag |should| be(True)
        result |should| have(1).elements
        faileds |should| be_empty

        response, item, queue = result[0]
        item.op_result |should| equal_to('SUCCESS')
        item.op_name |should| equal_to('update')

        queue = SyncQueue.objects(**{'operations.0.item_id': item.item_id}).get()
        expect_item = queue.operations[0]
        expect_item.item_id |should| equal_to(item.item_id)

    def test_check_one_static_file(self):
        processor = self.static_processor_class('css/main.css')
        flag, result, faileds = processor.publish()
        flag |should| be(True)
        result |should| have(1).elements
        faileds |should| be_empty

        flag, result, faileds = processor.check()
        response, item, queue = result[0]
        flag |should| be(True)
        result |should| have(1).elements
        faileds |should| be_empty
        item.op_name |should| equal_to('check')
        item.publish_path |should| equal_to(item.source_path)

        queue = SyncQueue.objects(**{'operations.0.item_id': item.item_id}).get()
        expect_item = queue.operations[0]
        expect_item.item_id |should| equal_to(item.item_id)

    def test_publish_many_static_file(self):
        processor = self.static_processor_class('css')
        flag, result, faileds = processor.publish()
        flag |should| be(True)
        result |should| have_at_least(3).elements
        faileds |should| be_empty

        response, item, queue = result[0]
        item.op_result |should| equal_to('SUCCESS')

        expect_queue = SyncQueue.objects(
            _id=queue.id,
            **{'operations.0.item_id': item.item_id}).get()
        expect_item = expect_queue.operations[0]
        expect_item.item_id |should| equal_to(item.item_id)


        expect_queues = SyncQueue.objects(content_type=queue.content_type,
                          object_pk=queue.object_pk)
        len(result) |should| equal_to(expect_queues.count())

    def test_delete_one_static_file(self):
        processor = self.static_processor_class('css/main.css')
        flag, result, faileds = processor.publish()
        flag |should| be(True)
        result |should| have(1).elements
        faileds |should| be_empty

        flag, result, faileds = processor.delete()
        response, item, queue = result[0]
        flag |should| be(True)
        result |should| have(1).elements
        faileds |should| be_empty
        item.op_name |should| equal_to('delete')
        item.publish_path |should| equal_to(item.source_path)

        queue = SyncQueue.objects(**{'operations.0.item_id': item.item_id}).get()
        expect_item = queue.operations[0]
        expect_item.item_id |should| equal_to(item.item_id)

    fixtures = [
        'syncqueue.json',
        'webservice-20140314-promotion.json',
        'webservice-20140314-taxonomy.json',
    ]

    def test_publish_version_one_file(self):
        from warehouse.models import PackageVersion
        pv = PackageVersion.objects.get(pk=615)

        processor = self.packageversion_processor_class(pv)
        print(pv.get_download().name)
        response, op_item, queue = processor.publish_one(pv.get_download().name)
        response.code |should| be(response.STATUS_CODE_SUCCESS)
        op_item.op_result |should| equal_to('SUCCESS')

        expect_queues = SyncQueue.objects(
            content_type=queue.content_type,
            object_pk=queue.object_pk
        )
        expect_queues.count() |should| equal_to(1)
        expect_item = expect_queues[0].operations[0]
        expect_item.item_id |should| equal_to(op_item.item_id)

    def test_publish_version_many_file(self):
        from warehouse.models import PackageVersion
        pv = PackageVersion.objects.get(pk=615)

        processor = self.packageversion_processor_class(pv)
        flag, result, faileds = processor.publish()
        flag |should| be(True)
        result |should| have_at_least(4).elements
        faileds |should| be_empty

        response, item, queue = result[0]
        item.op_result |should| equal_to('SUCCESS')

        expect_queue = SyncQueue.objects(
            _id=queue.id,
            **{'operations.0.item_id': item.item_id}).get()
        expect_item = expect_queue.operations[0]
        expect_item.item_id |should| equal_to(item.item_id)
        expect_queues = SyncQueue.objects(content_type=queue.content_type,
                                          object_pk=queue.object_pk)
        len(result) |should| equal_to(expect_queues.count())

    def test_after_save_packageversion_call_to_publish(self):
        from warehouse.models import PackageVersion
        pv = PackageVersion.objects.get(pk=615)
        pv.save()

    def test_after_save_adv(self):
        from promotion.models import Advertisement
        adv = Advertisement.objects.get(pk=10)
        adv.save()

    def test_after_save_topic(self):
        from taxonomy.models import Topic
        topic = Topic.objects.get(pk=12)
        topic.save()

    def test_after_save_category(self):
        from taxonomy.models import Category
        category = Category.objects.get(slug='big-game')
        category.save()

    def test_after_save_packageversion_call_to_publish_and_feedback(self):
        from warehouse.models import PackageVersion
        pv = PackageVersion.objects.get(pk=615)
        pv.save()

        ct = PackageVersionProcessor.content_type_to_db(pv)
        queue = SyncQueue.objects(content_type=ct, object_pk=str(pv.pk)).get()
        op = queue.operations[0]

    def test_publish_one_static_file_and_feedback(self):
        from website.cdn import feedback_signals as fb_signals
        def feedback_start_action(sender, instance, operation, queue, **kwargs):
            print(queue)
            pass
        fb_signals.start_action.connect(feedback_start_action, sender=self.feedback_class)

        processor = self.static_processor_class('css/main.css')
        flag, result, faileds = processor.publish()
        flag |should| be(True)
        result |should| have(1).elements
        faileds |should| be_empty

        response, op_item, queue = result[0]
        op_item.op_status = 'download finish'
        content = FeedbackContextParser.unparse_to_content([op_item])
        feedback = self.feedback_class()
        response = feedback.process(content)
        response.code |should| be(response.STATUS_CODE_SUCCESS)

    def test_publish_packageversion_files_and_feedback(self):
        from warehouse.models import PackageVersion
        pv = PackageVersion.objects.get(pk=615)

        processor = self.packageversion_processor_class(pv)
        flag, result, faileds = processor.publish()
        flag |should| be(True)
        result |should| have_at_least(4).elements
        faileds |should| be_empty
        response, op_item, queue = result[0]


        self.fb_func_called = False
        def feedback_model_action(sender, instance, operation, queue, **kwargs):
            self.fb_func_called = True

        fb_signals.start_model_action.connect(feedback_model_action,
                                              sender=PackageVersion)

        op_item.op_status = 'download finish'
        content = FeedbackContextParser.unparse_to_content([op_item])
        feedback = self.feedback_class()
        response = feedback.process(content)
        response.code |should| be(response.STATUS_CODE_SUCCESS)

        self.fb_func_called |should| be(True)

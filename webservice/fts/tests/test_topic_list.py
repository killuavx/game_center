from fts.tests.helpers import ApiDSL, RestApiTest
from warehouse.models import Package, PackageVersion, Author
from taxonomy.models import Topic
from django.utils.timezone import now, timedelta
from django.core.urlresolvers import reverse
from fts.middlewares import get_current_request

from pprint import pprint as print

class TopicListTest(RestApiTest):

    def _topic_with_some_packages(self, pkg_num=5, **defaults):
        today = now() - timedelta(minutes=10)
        topic = ApiDSL.Given_i_have_topic_with(self,all_datetime=today,
                                               status=Topic.STATUS.published,
                                               **defaults)
        for i in range(pkg_num):
            pkg = ApiDSL.Given_i_have_published_package(self,
                                        all_datetime=today-timedelta(seconds=2))
            ApiDSL.Given_topic_add_package(self, topic, pkg)

        return topic

    def test_list(self):
        topic = self._topic_with_some_packages(name='Choice Topics',
                                               slug='choice-topics')
        self.assertEqual(topic.is_published(), True)
        topic1 = self._topic_with_some_packages(name='handle game')
        topic.children.add(topic1)
        self.assertEqual(topic1.is_published(), True)

        topic2 = self._topic_with_some_packages(name='ea')
        topic.children.add(topic2)
        self.assertEqual(topic2.is_published(), True)

        except_topic = Topic.objects.get(pk=topic.pk)
        self.assertEqual(except_topic.children.count(), 2)
        self.assertEqual(except_topic.children.all()[0], topic1)
        self.assertEqual(except_topic.children.all()[1], topic2)

        ApiDSL.When_i_access_topic_list(self, topic)
        ApiDSL.Then_i_should_receive_success_response(self)
        content = self.world.get('content')
        self.assertResultList(content, previous=None, next=None,
                              count=2, result_len=2)

        ApiDSL.Then_i_should_see_topic_list(self, content.get('results'))

    def test_detail(self):
        topic = self._topic_with_some_packages(name='Newest',
                                               slug='newest')
        self.assertEqual(topic.is_published(), True)
        ApiDSL.When_i_access_topic_detail(self, topic)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_topic_detail(self, self.world.get('content'))


    def _page_url(self, name, topic, page=1):
        req = get_current_request()
        return req.build_absolute_uri(
            reverse(name,
                    kwargs=dict(slug=topic.slug)
            )
        ) + '?page=%d' %page

    def test_package_item_list(self):
        # TODO 专区软件列表查询
        topic = self._topic_with_some_packages(
            name='精选推荐',
            slug='index-recommend-packages',
            pkg_num=15)
        self.assertEqual(topic.items.count(), 15)
        self.assertEqual(topic.is_published(), True)
        ApiDSL.When_i_access_topic_items(self, topic)
        ApiDSL.Then_i_should_receive_success_response(self)
        pkgs = ( tp.content_object for tp in topic.items.all() )
        for p in pkgs:
            self.assertEqual(p.is_published(), True)

        prev_url = None
        next_url = self._page_url('topic-items', topic, page=2)
        ApiDSL.Then_i_should_see_result_list(self,
                                             num=10, count=15,
                                             previous=prev_url, next=next_url)

    def test_author_item_list(self):
        # TODO 顶级开发商列表
        pass

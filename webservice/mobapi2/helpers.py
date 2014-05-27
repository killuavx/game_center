# -*- encoding: utf-8-*-
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.http import urlencode
from django.utils.importlib import import_module
from comment.models import Comment


def import_module_member(member_name, module_name):
    module = import_module(module_name)
    return module.__dict__.get(member_name)


def topic_viewset_model_map():
    _topic_viewset_model_default = [import_module_member('PackageViewSet',
                                                         'mobapi2.warehouse.views.package'),
                                    import_module_member('Package',
                                                         'warehouse.models'),
                                    '默认游戏专区']
    _topic_viewset_model_author = [import_module_member('AuthorViewSet',
                                                        'mobapi2.warehouse.views.author'),
                                   import_module_member('Author',
                                                        'warehouse.models'),
                                   '默认游戏专区']
    _topic_viewset_model_map = {
        'default': _topic_viewset_model_default,
        # - 精选推荐
        'home-recommend-game': _topic_viewset_model_default,
        # - 网游专区
        'home-network-game': _topic_viewset_model_default,

        # - 最新游戏
        'homebar-newest-game': _topic_viewset_model_default,
        # - 大型游戏
        'homebar-big-game': _topic_viewset_model_default,
        # - 中文游戏
        'homebar-cn-game': _topic_viewset_model_default,
        # -- 精选专辑
        'spec-choice-topic': _topic_viewset_model_default,
        # -- 顶级开发商
        'spec-top-author': _topic_viewset_model_author,
    }
    return _topic_viewset_model_map


def get_basic_topic_info():
    new_map = {}
    for slug, _map in topic_viewset_model_map().items():
        new_map[slug] = _map[2]
    return new_map


def get_item_model_by_topic(topic):
    vsm_map = topic_viewset_model_map()
    try:
        return vsm_map[topic.slug][1]
    except KeyError:
        return vsm_map['default'][1]


def get_viewset_by_topic(topic):
    vsm_map = topic_viewset_model_map()
    try:
        return vsm_map[topic.slug][0]
    except KeyError:
        return vsm_map['default'][0]


def get_packageversion_comment_queryset(version):
    return Comment.objects.for_model(version).visible()


def get_packageversion_comments_url(version, router=None):
    ct = ContentType.objects.get_for_model(version)
    kwargs = dict(content_type=ct.pk, object_pk=version.pk)
    view_name = router.get_base_name('comment-list') if router else 'comment-list'
    url = reverse(view_name)
    return "%s?%s" % (url, urlencode(kwargs))


def get_object_star(obj):
    return round(obj.stars_average, 1)


def get_object_stars_rate(obj, rate_type):
    """
        rate_type in (good, medium, low)
    """
    rate = getattr(obj, 'stars_%s_rate'%rate_type, 0)
    return round(rate, 3)


def make_cache_key(prefix, app='api'):
    return "%s.%s" %(app, prefix)


from urllib import parse


class BaseWarehouseApiUrlEncode(object):

    viewname = None

    topic_param = 'topic_slug'
    topic = None

    ordering = None
    ordering_param = 'ordering'

    def __init__(self, request=None, router=None, **kwargs):
        self.request = request
        self.router = router

        self.topic = kwargs.get('topic')
        self.ordering = kwargs.get('ordering')

    def reverse_path(self):
        if self.router:
            reverse_viewname = self.router.get_base_name(self.viewname)
        else:
            reverse_viewname = self.viewname
        return reverse(reverse_viewname)

    def get_queryparams(self, qp=None):
        if qp is None:
            qp = []

        if self.topic:
            qp.append((self.topic_param, self.topic.slug))

        if self.ordering:
            qp.append((self.ordering_param, self.ordering))

        return qp

    def get_url(self):
        path = self.reverse_path()
        urlp = list(parse.urlparse(path))
        qp = parse.parse_qsl(urlp[4])

        qp = self.get_queryparams(qp)

        urlp[4] = parse.urlencode(qp, True)
        url = parse.urlunparse(urlp)
        if self.request:
            return self.request.build_absolute_uri(url)
        return url


class AuthorListApiUrlEncode(BaseWarehouseApiUrlEncode):

    viewname = 'author-list'


class PackageListApiUrlEncode(BaseWarehouseApiUrlEncode):

    viewname = 'package-list'

    category_param = 'categories'
    category = None

    def __init__(self, **kwargs):
        super(PackageListApiUrlEncode, self).__init__(**kwargs)
        self.category = kwargs.get('category')

    def get_queryparams(self, qp=None):
        qp = super(PackageListApiUrlEncode, self).get_queryparams(qp)
        if self.category:
            qp.append((self.category_param, self.category.pk))
        return qp


def get_category_packages_url(category, ordering=None, router=None, request=None):
    if ordering is None:
        ordering = '-released_datetime'
    apiencode = PackageListApiUrlEncode(category=category,
                                        ordering=ordering,
                                        request=request,
                                        router=router)
    url = apiencode.get_url()
    print(url)
    return url


def get_topic_packages_url(topic, ordering=None, router=None, request=None):
    if ordering is None:
        ordering = 'topical'
    apiencode = PackageListApiUrlEncode(topic=topic,
                                        ordering=ordering,
                                        request=request,
                                        router=router)
    url = apiencode.get_url()
    print(url)
    return url


def get_topic_authors_url(topic, ordering=None, router=None, request=None):
    if ordering is None:
        ordering = 'topical'
    apiencode = AuthorListApiUrlEncode(topic=topic,
                                       ordering=ordering,
                                       request=request,
                                       router=router)
    url = apiencode.get_url()
    print(url)
    return url

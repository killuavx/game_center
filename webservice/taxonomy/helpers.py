# -*- encoding=utf-8 -*-

def slugify(text=""):
    return text.replace(" ", "-").lower()

from warehouse.models import Package, Author
from mobapi.views import PackageViewSet, AuthorViewSet
_topic_viewset_model_map = {
    'default' : (PackageViewSet, Package, '默认游戏专区') ,

    # - 精选推荐
    'home-recommend-game': (PackageViewSet, Package , '精选推荐'),
    # - 网游专区
    'home-network-game':  (PackageViewSet, Package, '网游专区') ,

    # - 最新游戏
    'homebar-newest-game': (PackageViewSet, Package, '最新游戏'),
    # - 大型游戏
    'homebar-big-game': (PackageViewSet, Package, '大型游戏'),
    # - 中文游戏
    'homebar-cn-game': (PackageViewSet, Package, '中文游戏'),

    # -- 精选专辑
    'spec-choice-topic': (PackageViewSet, Package, '精选专辑'),
    # -- 顶级开发商
    'spec-top-author': (AuthorViewSet, Author, '顶级开发商'),
    }

def get_basic_topic_info():
    new_map = {}
    for slug, _map in _topic_viewset_model_map.items():
        new_map[slug]=_map[2]
    return new_map

def get_item_model_by_topic(topic):
    try:
        return _topic_viewset_model_map[topic.slug][1]
    except KeyError:
        return _topic_viewset_model_map['default'][1]

def get_viewset_by_topic(topic):
    try:
        return _topic_viewset_model_map[topic.slug][0]
    except KeyError:
        return _topic_viewset_model_map['default'][0]


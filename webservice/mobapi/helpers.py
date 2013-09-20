# -*- encoding: utf-8-*-
from django.utils.importlib import import_module

def import_module_member(member_name, module_name):
    module = import_module(module_name)
    return module.__dict__.get(member_name)

def topic_viewset_model_map():
    _topic_viewset_model_default = [
                                       import_module_member('PackageViewSet',
                                                            'mobapi.views'),
                                       import_module_member('Package',
                                                            'warehouse.models' ),
                                       '默认游戏专区'
                                   ]
    _topic_viewset_model_author = [
                                      import_module_member('AuthorViewSet',
                                                           'mobapi.views'),
                                      import_module_member('Author',
                                                           'warehouse.models' ),
                                      '默认游戏专区'
                                  ]
    _topic_viewset_model_map = {
        'default' : _topic_viewset_model_default,
        # - 精选推荐
        'home-recommend-game': _topic_viewset_model_default,
        # - 网游专区
        'home-network-game':  _topic_viewset_model_default,

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
        new_map[slug]=_map[2]
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



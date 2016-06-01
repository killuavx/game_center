# -*- coding: utf-8 -*-
import os
import sh
import json
from account.settings import UC_CLIENT_CMD


def generate_interfaces():
    import yaml
    fname = os.path.join(os.path.dirname(__file__), 'uc_client.yaml')
    with open(fname, 'r') as f:
        return yaml.load(f)


class UcenterError(Exception):
    errors = ('Access denied for agent changed',
              'Module not found!',
              'Action not found!')


class UcenterApiNotFound(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "ucenter api %s not exists." % self.name


class ClientApi(object):
    """
        访问ucenter接口client，采用shell方式直接访问
    """

    def __init__(self, *args, **kwargs):
        self.uc_client_api = sh.php.bake('-f', UC_CLIENT_CMD)
        self.interfaces = generate_interfaces()

    def uc_api_shell(self, action, **kwargs):
        _in = self.parse_args(action, **kwargs)
        _out = str(self.uc_client_api(action, _in=_in))
        return self.parse_return(action, _out)

    def parse_args(self, action, **kwargs):
        _args_list = list()
        for arg in self.interfaces[action]['args']:
            arg_name = arg['name']
            if arg_name not in kwargs:
                val = arg.get('default')
            else:
                val = kwargs.get(arg_name)
            _args_list.append(val)
        return json.dumps(_args_list)

    def parse_return(self, action, result):
        return json.loads(result)

    def __getattr__(self, name):
        if name not in self.interfaces:
            raise AttributeError('ClientApi has not attribute: %s'% name)

        def _ucwrapper(**kwargs):
            try:
                return self.uc_api_shell(name, **kwargs)
            except sh.ErrorReturnCode_127:
                raise UcenterApiNotFound(name)

        return _ucwrapper


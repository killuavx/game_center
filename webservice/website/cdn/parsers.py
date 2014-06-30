# -*- coding: utf-8 -*-
import hashlib
import json
from xml.etree import cElementTree as ET

from django.utils.encoding import force_str, force_bytes
from django.core.urlresolvers import reverse_lazy
import requests
from .errors import RequestProcessException, NotDefineOperationError


CUST_ID = '6807'

PASSWD = 'EYjgz9PNhF'


def create_element(tagname, text=None, attrs=dict(), parent=None):
    if parent is not None:
        e = ET.SubElement(parent, tagname)
    else:
        e = ET.Element(tagname)
    if text is not None:
        e.text = str(text)
    for key, val in attrs.items():
        e.set(key, str(val))
    return e


class SyncItemParser(object):

    def __init__(self, operation):
        self.operation = operation

    def parse_to_item(self):
        pass


class UpdateItemParser(SyncItemParser):

    def parse_to_item(self):
        operation = self.operation
        el_item_id = create_element('item_id', attrs=dict(value=operation.item_id))
        create_element('source_path', operation.source_path, parent=el_item_id)
        create_element('publish_path', operation.publish_path, parent=el_item_id)
        create_element('file_size', operation.file_size, parent=el_item_id)
        create_element('md5', operation.md5, el_item_id)
        return el_item_id


class PublishItemParser(SyncItemParser):

    def parse_to_item(self):
        operation = self.operation
        el_item_id = create_element('item_id', attrs=dict(value=operation.item_id))
        create_element('source_path', operation.source_path, parent=el_item_id)
        create_element('publish_path', operation.publish_path, parent=el_item_id)
        create_element('file_size', operation.file_size, parent=el_item_id)
        create_element('md5', operation.md5, el_item_id)
        create_element('filelevel', operation.filelevel, parent=el_item_id)
        return el_item_id


class DeleteItemParser(SyncItemParser):

    def parse_to_item(self):
        operation = self.operation
        el_item_id = create_element('item_id', attrs=dict(value=operation.item_id))
        create_element('source_path', operation.source_path, parent=el_item_id)
        create_element('publish_path', operation.publish_path, parent=el_item_id)
        return el_item_id


class RenameItemParser(SyncItemParser):

    def parse_to_item(self):
        operation = self.operation
        el_item_id = create_element('item_id', attrs=dict(value=operation.item_id))
        create_element('source_path', operation.source_path, parent=el_item_id)
        create_element('publish_path', operation.publish_path, parent=el_item_id)
        return el_item_id


class CheckItemParser(SyncItemParser):

    def parse_to_item(self):
        operation = self.operation
        el_item_id = create_element('item_id', attrs=dict(value=operation.item_id))
        create_element('source_path', operation.source_path, parent=el_item_id)
        create_element('publish_path', operation.publish_path, parent=el_item_id)
        create_element('file_size', operation.file_size, parent=el_item_id)
        create_element('md5', operation.md5, parent=el_item_id)
        return el_item_id


class UnzipItemParser(SyncItemParser):

    def parse_to_item(self):
        operation = self.operation
        el_item_id = create_element('item_id', attrs=dict(value=operation.item_id))
        create_element('publish_path', operation.publish_path, parent=el_item_id)
        return el_item_id


ITEM_PARSERS = {
    'publish': PublishItemParser,
    'update': UpdateItemParser,
    'delete': DeleteItemParser,
    'rename': RenameItemParser,
    'check': CheckItemParser,
    'unzip': UnzipItemParser
}


class OperationResponse(object):

    STATUS_CODE_SUCCESS = 1

    STATUS_CODE_FAILED = 0

    STATUS_CODES = {
        STATUS_CODE_SUCCESS: 'SUCCESS',
        STATUS_CODE_FAILED: 'FAILED'
    }

    code = None

    result = None

    detail = None

    def __init__(self, code=None, detail=''):
        self.code = code
        self.detail = detail

    @classmethod
    def from_xmlstring(cls, content=''):
        root = ET.fromstring(content)
        result = root.find('result').text
        detail = root.find('detail').text
        code = cls.result_code(result)
        response = cls(code, detail)
        response.result = result
        return response

    @classmethod
    def result_code(cls, result):
        for code, expect_result in cls.STATUS_CODES.items():
            if expect_result == result:
                return code
        return None

    @classmethod
    def result_string(cls, code):
        return cls.STATUS_CODES[code]

    def to_xmlstring(self):
        root = create_element('ccsc')
        result = self.result_string(self.code)
        create_element('reuslt', result, parent=root)
        create_element('detail', self.detail, parent=root)
        return ET.tostring(root, 'utf-8', 'xml')

    def render(self):
        return self.to_xmlstring()


class OperationRequest(object):

    request_url = 'http://centre.fds.ccgslb.net:8080/fds/soap/receiveTask.php'

    cust_id = CUST_ID

    passwd = PASSWD

    ITEM_PARSERS = ITEM_PARSERS

    response_class = OperationResponse

    def __init__(self, op_item):
        self.op_item = op_item
        if op_item.op_name not in self.ITEM_PARSERS:
            raise NotDefineOperationError()
        self.item_parser_class = self.ITEM_PARSERS[op_item.op_name]

    def generate_passwd_hash(self):
        passwd_text = '%s%s%s%s' % (self.op_item.item_id, self.cust_id,
                                    'chinacache', self.passwd)
        return hashlib.md5(force_bytes(passwd_text)).hexdigest()

    def create_context(self):
        root=ET.Element('ccsc')
        el_cust = create_element('cust_id', self.cust_id)
        el_pwd = create_element('passwd', self.generate_passwd_hash())
        root.append(el_cust)
        root.append(el_pwd)
        el_item = self.item_parser_class(self.op_item).parse_to_item()
        root.append(el_item)
        return force_str(ET.tostring(root, 'utf8'))

    def create_querydata(self):
        return dict(
            op=self.op_item.op_name,
            context=self.create_context()
        )

    def request(self):
        data = self.create_querydata()
        response = requests.post(self.request_url, data)
        if response.status_code != requests.codes.get('ok'):
            raise RequestProcessException(response.status_code)

        response = self.response_class.from_xmlstring(response.content)
        return response


class FeedbackItem(object):
    """op_status 项内容说明:
       sync finish 指文件分发成功,客户可以发布
￼￼￼￼￼￼￼delete finish 指删除文件成功,客户可以发布
￼￼￼￼￼￼￼rename finish 指文件改名成功
￼￼￼￼￼￼￼unzip finish 指解压完成
￼￼￼￼￼￼￼unzip failed 指解压失败
    """

    STATUS_SUCCESS = 'SUCCESS'

    STATUS_FAILED = 'FAILED'

    def __init__(self, item_id, op_name, op_status):
        self.item_id = item_id
        self.op_name = op_name
        self.op_status = op_status
        if 'finish' in op_status:
            self.fb_result = self.STATUS_SUCCESS
        elif 'failed' in op_status:
            self.fb_result = self.STATUS_FAILED


class FeedbackContextParser(object):
    """<?xml version="1.0" encoding="UTF-8"?>
    <ccsc>
        <item_id value="1234567">
            <op_name>publish</op_name>
            <op_status>
                (download failed| download finish | sync finish)
            </op_status>
        </item_id>
        <item_id value="565321">
            <op_name>unzip</op_name>
            <op_status>
                (unzip finish | unzip failed)
            </op_status>
        </item_id>
    </ccsc>
    """

    feedback_item_class = FeedbackItem

    @classmethod
    def parse(cls, content):
        return cls.parse_from_content(content=content)

    @classmethod
    def parse_from_content(cls, content=''):
        """
            str content

            return list<FeedbackItem>
        """
        root = ET.fromstring(content)
        items = []
        for item in root.findall('item_id'):
            items.append(cls.parse_item(item))
        return items

    @classmethod
    def unparse_to_content(cls, op_items):
        """
            list<cdn.BaseOperation> op_items

            return str
        """
        root = create_element('cscc')
        for item in op_items:
            el_item = create_element('item_id', attrs=dict(value=item.item_id))
            create_element('op_name', item.op_name, parent=el_item)
            create_element('op_status', item.op_status, parent=el_item)
            root.append(el_item)
        return ET.tostring(root, 'utf-8')

    @classmethod
    def parse_item(cls, item):
        return cls.feedback_item_class(
            item_id=item.get('value'),
            op_name=item.find('op_name').text,
            op_status=item.find('op_status').text
        )


class RefreshRequest(object):

    request_url = 'https://r.chinacache.com/content/refresh'

    username = CUST_ID

    password = PASSWD

    def __init__(self, task):
        """
        刷新任务,JSON 格式例子:
            {
            "urls":["http://www.xxx.com/logo.gif","http://www.xxx.com/"],
            "dirs":["http://www.xxx.com/imgs/","http://www.xxx.com/html/"],
            "callback":{"url":"http://xxx.com/listener",
                        "email":["a@a.com","b@a.com"],
                        "acptNotice":true}
            }
        urls 是需要刷新的 url 的地址,可以是多个,最多支持 100 条。
        dirs 是需要刷新的目录的地址,最多支持 10 条。
        callback 是接收刷新执行结果反馈的地址和电子邮箱,如果值为空或没有 callback 属 性,表示不接收反馈。
        url 表示接收反馈的地址,可以为空。
        email 表示接收反馈的电子邮箱,可以为空。
        acptNotice 表示接收成功时是否反馈,仅在 email 有效时有效。 当 url 和 email 都为空时,不反馈。
        """
        self.task = task

    def create_querydata(self):
        return dict(username=self.username,
                    password=self.password,
                    task=json.dumps(self.task))

    def request(self):
        data = self.create_querydata()
        response = requests.post(url=self.request_url, data=data)
        if response.status_code != requests.codes.get('ok'):
            raise RequestProcessException(response.status_code)
        return response


class RefreshTask(dict):

    def __init__(self, urls=None, dirs=None, callback=None, *args):
        super(RefreshTask, self).__init__()
        if urls:
            self['urls'] = urls
        if dirs:
            self['dirs'] = dirs
        if callback:
            self['callback'] = callback


class RefreshResponse(object):

    STATUS_CODE_SUCCESS = 1

    STATUS_CODE_FAILED = 0

    STATUS_CODE_UNKNOW = -1

    STATUS_CODES = {
        STATUS_CODE_SUCCESS: 'SUCCESS',
        STATUS_CODE_FAILED: 'FAIL',
        STATUS_CODE_UNKNOW: 'UNKNOW'
    }

    code = None

    detail = None

    result = None

    instance = None

    def __init__(self, code=None, detail=''):
        self.code = code
        self.detail = detail

    @classmethod
    def from_refresh_queue(cls, refresh_queue):
        code = cls.result_code(refresh_queue.status)
        response = cls(code, refresh_queue.status)
        response.instance = refresh_queue
        response.result = refresh_queue.url_status
        return response

    @classmethod
    def result_code(cls, result):
        for code, expect_result in cls.STATUS_CODES.items():
            if expect_result == result:
                return code
        return None

    @classmethod
    def result_string(cls, code):
        return cls.STATUS_CODES[code]

    @property
    def content_object(self):
        if self.instance:
            return self.instance.content_object
        return None

    def render(self):
        return dict(code=self.code)
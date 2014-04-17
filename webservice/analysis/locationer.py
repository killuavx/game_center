# -*- coding: utf-8 -*-
from .models import UNDEFINED
import requests
from .documents.event import CellTower
from mongoengine import fields, Document, DoesNotExist

"""
class CellTower(Document):

    mcc = fields.IntField()
    mnc = fields.IntField()
    lac = fields.IntField()
    cid = fields.IntField(unique_with=['mcc', 'mnc', 'lac'])

    lng = fields.FloatField()
    lat = fields.FloatField()

    point = fields.GeoPointField()

    samples = fields.IntField(default=0)
    changeable = fields.BooleanField(default=False)

    created = fields.DateTimeField(default=None)
    updated = fields.DateTimeField(default=None)

    averageSignalStrength = fields.FloatField(default=0)

    meta = {
        'collection': 'cell_tower',
        'indexes': [
            'mcc',
            ('mcc', 'mnc'),
            ('mcc', 'mnc', 'lac', 'cid'),
            ]
    }
"""


BAIDU_AK = 'B639412ddc60cf3099c8c3b2ea249ce0'


class Locationer(object):

    LOCATION_UNDEFINED = (UNDEFINED, UNDEFINED, UNDEFINED)

    LOCATION_DOMESTIC = ('中国', UNDEFINED, UNDEFINED)

    @classmethod
    def factory_locationer(cls, doc):
        if hasattr(doc, 'network') and doc.network == 'wifi' and hasattr(doc, 'client_ip'):
            return IPLocationer(ip=doc.client_ip)
        elif hasattr(doc, 'client_ip'):
            return IPLocationer(ip=doc.client_ip)
        elif hasattr(doc, 'cell'):
            return CellTowerLocationer(cell=doc.cell)
        return None

    @classmethod
    def get_or_save_address(cls, doc):
        if hasattr(doc, 'address'):
            return doc.address
        else:
            locationer = cls.factory_locationer(doc)
            if locationer:
                doc.address = locationer.get_location()
                doc.save()
                return doc.address
            return None


class IPLocationer(Locationer):

    ak = BAIDU_AK

    coor = 'bd09ll'

    api_url = 'http://api.map.baidu.com/location/ip'

    ip = None

    def __init__(self, ip):
        self.ip = ip

    def request_location(self, ip):
        response = requests.get(self.api_url,
                                params=dict(ak=self.ak, coor=self.coor, ip=ip))
        if response.status_code == 200:
            result = response.json()
            if result and result.get('status') == 0:
                content = result.get('content', dict())
                return self.to_geolocation(content)
        return None

    def get_dimension_data(self, ip):
        addr = self.request_location(ip)
        if addr:
            return addr['country'], addr['province'], addr['city']
        else:
            return self.LOCATION_UNDEFINED

    def to_geolocation(self, content):
        detail = content.get('address_detail')
        country = self.LOCATION_DOMESTIC[0]
        province = detail.get('province') or self.LOCATION_DOMESTIC[1]
        city = detail.get('city') or self.LOCATION_DOMESTIC[2]
        detail.update(
            country=country,
            province=province,
            city=city,
            city_code=content.get('city_code')
        )
        point = content.get('point')
        detail['point'] = [float(point.get('x', 0)), float(point.get('y', 0))]
        return detail

    def get_location(self):
        return self.request_location(self.ip)


class CellTowerLocationer(Locationer):

    ak = BAIDU_AK

    api_url = 'http://api.map.baidu.com/geocoder/v2/'

    output = 'json'

    coordtype = 'bd09ll'

    pois = 0

    cell = dict(
        mnc=None,
        mcc=460,
        lac=None,
        cid=None
    )

    def __init__(self, cell):
        self.cell = cell

    def request_location(self, lat, lng):
        response = requests.get(self.api_url,
                                params=dict(
                                    ak=self.ak,
                                    output=self.output,
                                    coordtype=self.coordtype,
                                    pois=self.pois,
                                    location=",".join([lat, lng])
                                ))
        if response.status_code == 200:
            result = response.json()
            if result and result.get('status') == 0:
                content = result.get('result', dict())
                addr = self.to_geolocation(content)
                return addr
        return None

    def to_geolocation(self, content):
        detail = content.get('addressComponent', dict())
        country = self.LOCATION_DOMESTIC[0]
        province = detail.get('province') or self.LOCATION_DOMESTIC[1]
        city = detail.get('city') or self.LOCATION_DOMESTIC[2]
        detail.update(
            country=country,
            province=province,
            city=city,
            city_code=content.get('cityCode')
        )
        point = content.get('location', dict(lat=0, lng=0))
        detail['point'] = [float(point['lat']), float(point['lng'])]
        return detail

    def get_dimension_data(self, mnc, mcc, lac, cid):
        try:
            cell = CellTower.objects \
                .filter(mnc=mnc, mcc=mcc, lac=lac, cid=cid).get()
        except DoesNotExist:
            return self.LOCATION_UNDEFINED
        else:
            lat, lng = cell.point[0], cell.point[1]
            addr = self.request_location(lat=lat, lng=lng)
            if addr:
                return addr['country'], addr['province'], addr['city']
            else:
                return self.LOCATION_UNDEFINED

    def get_location(self):
        try:
            cell = CellTower.objects \
                .filter(mnc=self.cell['mnc'],
                        mcc=self.cell['mcc'],
                        lac=self.cell['lac'],
                        cid=self.cell['cid']).get()
        except DoesNotExist:
            return None
        else:
            lat, lng = cell.point[0], cell.point[1]
            return self.request_location(lat=lat, lng=lng)



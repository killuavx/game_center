# -*- coding: utf-8 -*-
import csv
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from crawler.models import IOSAppData, IOSBuyInfo

def import_buyinfo(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            buy, created = IOSBuyInfo.objects.get_or_create(
                id=row[0],
                appid=row[1],
                defaults=dict(
                    account=row[2],
                    ipafile_name=row[3],
                    ipafile=row[4],
                )
            )
            if not buy.appdata_id:
                qs = IOSAppData.objects.filter(appid=buy.appid)
                try:
                    buy.appdata = qs[0]
                except (IndexError, ObjectDoesNotExist) as e:
                    print(e)
                    pass
                buy.updated = now()
            else:
                package_name, version, short_version = buy.ipafile_name\
                    .rstrip('.ipa').split('_')
                buy.version = version
                buy.short_version = short_version
                buy.updated = now()
            buy.save()

from os.path import join, dirname, abspath

file = join(dirname(abspath(__file__)), 'buyinfo20140531.csv')




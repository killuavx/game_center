# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from hashlib import md5
from django.utils.encoding import force_bytes
from dateutil.parser import parse as dateparse
from optparse import make_option
from copy import deepcopy
from logging import getLogger
from analysis.etl import (
    LoadResultTask,
    LoadSumActivateDeviceProductsResultTask,
    LoadSumActivateDeviceProductPackagesResultTask,
    LoadSumActivateDeviceProductPackageVersionsResultTask,
    LoadSumDownloadProductResultTask)

logger = getLogger('scripts')

cycle_types = deepcopy(LoadResultTask.CHOICE_CYCLE_TYPE)
cycle_types['all'] = -1


RUN_CHOICES = ['sum_activate', 'sum_download']


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--run',
                    choices=RUN_CHOICES,
                    type='choice',
                    dest='run',
                    help='执行任务名 %s' % RUN_CHOICES
        ),
        make_option('--date',
                    type='string',
                    dest='date',
                    help='计算的当日的时间，'
                         '可配合daysago/until作为时间区间使用'
        ),
        make_option('--cycle_type',
                    choices=list(cycle_types.keys()),
                    dest='cycle_type',
                    type='choice',
                    default='all',
                    help="汇总(sum)统计的执行周期 %s" %list(cycle_types.keys())
        ),
        make_option('--task_type',
                    choices=['0', '1', '2', '3'],
                    dest='task_type',
                    type='choice',
                    default='0',
                    help="任务类型, 用于sum_activate汇总数据的粒度类型, "
                         "可选类型 all:0, product:1, product-package:2, product-package-version:3",
        ),
    )
    can_import_settings = True

    def handle(self, *args, **options):
        self.set_hash(now=datetime.now(), opts=options)
        self.log_start(options)
        if not options['run']:
            msg = 'date必须提供'
            self.log_info(msg)
            self.log_end()
            raise CommandError(msg)
        if not options['date']:
            msg = 'date必须提供'
            self.log_info(msg)
            self.log_end()
            raise CommandError(msg)

        try:
            opt_date = dateparse(options['date'])
        except ValueError:
            msg = '日期格式错误 date: %s' % options['date']
            self.log_info(msg)
            self.log_end()
            raise CommandError(msg)

        action_name = options['run']
        if not hasattr(self, 'run_%s' % action_name):
            msg = '没有可执行的任务 %s' %action_name
            self.log_info(msg)
            self.log_end()
            raise CommandError(msg)

        if action_name == 'sum_activate':
            self.run_sum_activate(opt_date, options['cycle_type'], options['task_type'])
        elif action_name == 'sum_download':
            self.run_sum_download(opt_date, options['cycle_type'])
        else:
            self.log_info('Invalid options')

        self.log_end()

    def set_hash(self, **kwargs):
        m = md5()
        m.update(force_bytes(kwargs))
        self.hash_idx = m.hexdigest()

    def log_start(self, options):
        logger.info('COMMAND %s START analysis.management.commands.run_sum'
                    'Process' % self.hash_idx)
        logger.info('COMMAND %s Options:' % self.hash_idx)
        logger.info(options)

    def log_end(self):
        self.log_info('END')

    def log_info(self, string):
        logger.info('COMMAND %s %s' % (self.hash_idx, string))

    def run_sum_activate(self, dt, cycle_type='all', task_type=-1):
        tasks = list()
        task_type = int(task_type)
        if task_type == 1 or task_type == 0:
            tasks.append(LoadSumActivateDeviceProductsResultTask())
        if task_type == 2 or task_type == 0:
            tasks.append(LoadSumActivateDeviceProductPackagesResultTask())
        if task_type == 3 or task_type == 0:
            tasks.append(LoadSumActivateDeviceProductPackageVersionsResultTask())

        if cycle_type == 'all':
            for t in tasks:
                t.process_daily(dt)
                t.process_weekly(dt)
                t.process_monthly(dt)
        elif cycle_type == 'daily':
            for t in tasks:
                t.process_daily(dt)
        elif cycle_type == 'weekly':
            for t in tasks:
                t.process_weekly(dt)
        elif cycle_type == 'monthly':
            for t in tasks:
                t.process_monthly(dt)

    def run_sum_download(self, dt, cycle_type='all'):
        task = LoadSumDownloadProductResultTask()
        self.log_info(dt)
        self.log_info(cycle_type)
        if cycle_type == 'daily':
            task.process_daily(dt)
        elif cycle_type == 'weekly':
            task.process_weekly(dt)
        elif cycle_type == 'monthly':
            task.process_monthly(dt)
        elif cycle_type == 'all':
            task.process_daily(dt)
            task.process_weekly(dt)
            task.process_monthly(dt)



# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from hashlib import md5
from django.utils.encoding import force_bytes
from dateutil.parser import parse as dateparse
from optparse import make_option
from copy import deepcopy
from logging import getLogger
from analysis.etl import (
    TransformActivateFactFromUsinglogFactTask,
    UsinglogETLProcessor, TransformDownloadFactFromUsinglogFactTask)

logger = getLogger('scripts')


RUN_CHOICES = ['usinglog', 'activate', 'download']


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
        make_option('--daysago',
                    type='int',
                    dest='daysago',
                    help='date的前几天，'
                         '如"--date=2014-04-15 --daysago=2"就是统计[2014-04-13, 2014-04-15)，'
                         '注意不能与until一起使用'
        ),
        make_option('--until',
                    type='string',
                    dest='until',
                    default='',
                    help='date之后结束日期，'
                         '如"--date=2014-04-10 --until=2014-04-15"就是[2014-04-10, 2014-04-15)'
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

        try:
            opt_until = dateparse(options['until']) if options['until'] else False
        except ValueError:
            msg = '日期格式错误 until: %s' % options['date']
            self.log_info(msg)
            self.log_end()
            raise CommandError(msg)

        opt_daysago = options['daysago']
        if opt_until is not None and opt_daysago is not None:
            msg = 'daysago, until不能同时使用'
            self.log_info(msg)
            self.log_end()
            raise CommandError(msg)

        if opt_until:
            start_dt = opt_date
            end_dt = opt_until
        elif opt_daysago:
            start_dt = opt_date - timedelta(days=opt_daysago)
            end_dt = opt_date
        else:
            msg = 'daysago/until 二选一'
            self.log_info(msg)
            self.log_end()
            raise CommandError(msg)

        self.log_info("%s, %s" % (start_dt, end_dt))

        action_name = options['run']
        if not hasattr(self, 'run_%s' % action_name):
            msg = '没有可执行的任务 %s' %action_name
            self.log_info(msg)
            raise CommandError(msg)

        run = 'run_%s' % action_name
        if not hasattr(self, run):
            self.log_info('Invalid Run Name: %s' % action_name)

        run_func = getattr(self, run)
        run_func(start_dt, end_dt)

        self.log_end()

    def set_hash(self, **kwargs):
        m = md5()
        m.update(force_bytes(kwargs))
        self.hash_idx = m.hexdigest()

    def log_start(self, options):
        logger.info('COMMAND %s START analysis.management.commands.run_etl '
                    'Process' % self.hash_idx)
        logger.info('COMMAND %s Options:' % self.hash_idx)
        logger.info(options)

    def log_end(self):
        self.log_info('END')

    def log_info(self, string):
        logger.info('COMMAND %s %s' % (self.hash_idx, string))

    def run_usinglog(self, start_date, end_date):
        self.log_info("runing usinglog %s, %s" % (start_date, end_date))
        processor = UsinglogETLProcessor()
        processor.process_between(start_date=start_date, end_date=end_date)

    def run_activate(self, start_date, end_date):
        task = TransformActivateFactFromUsinglogFactTask()
        task.process_between_datetime(start_date, end_date)

    def run_download(self, start_date, end_date):
        task = TransformDownloadFactFromUsinglogFactTask()
        task.process_between_datetime(start_date, end_date)

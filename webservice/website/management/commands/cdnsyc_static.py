# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from optparse import make_option
from website.cdn.processors.base import StaticProcessor
from logging import getLogger
logger = getLogger('scripts')

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--relative_path',
                    type='string',
                    dest='relative_path',
                    default=False,
                    help='relative path'),
        make_option('--sync_type',
                    choices=['publish', 'update'],
                    dest='type',
                    type='choice',
                    default='publish',
                    help='Sync Type'),
    )
    can_import_settings = True


    def handle(self, *args, **options):
        op_type = options['type']
        relative_path = options['relative_path']
        logger.info('COMMAND START sync static')
        logger.info('Options:')
        logger.info(options)
        try:
            processor = StaticProcessor(relative_path)
            operation = getattr(processor, op_type)
            flag, results, faileds = operation()
            logger.info("result: %s, all:%s, fail: %s" %
                        (flag, len(results), len(faileds)))
            logger.info('end sync process')
        except Exception as e:
            logger.info('COMMAND Exception: %s' %e)
        logger.info('COMMAND END sync static')

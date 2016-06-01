# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from warehouse.models import PackageVersion, Package
from optparse import make_option
from logging import getLogger
logger = getLogger('scripts')

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--random',
                    action='store_true',
                    dest='is_random',
                    default=False,
                    help='Random sync'),
        make_option('--limit',
                    dest='int',
                    default=1,
                    help='Random sync'),
        make_option('--package_name',
                    type='string',
                    dest='package_name',
                    default='',
                    help='Package Name'),
        make_option('--package_id',
                    type='int',
                    dest='package_id',
                    default=0,
                    help='Package.id'),
        make_option('--version_name',
                    type='string',
                    dest='version_name',
                    default=False,
                    help='PackageVersion.version_name with package'),
        make_option('--version_id',
                    type='int',
                    dest='version_id',
                    default=0,
                    help='PackageVersion.id'),
        make_option('--version_code',
                    type='int',
                    dest='version_code',
                    default=0,
                    help='PackageVersion.version_code with package'),
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
        logger.info('COMMAND START sync packageversion')
        logger.info('Options:')
        logger.info(options)
        if options['version_id']:
            version = self.get_packageversion(options, None)
            self.sync_processor(version, op_type)
        elif options['package_name'] or options['package_id']:
            package = self.get_package(options)
            version = self.get_packageversion(options, package)
            self.sync_processor(version, op_type)
        elif options['is_random']:
            versions = self.get_random_versions(options)
            for v in versions:
                self.sync_processor(v, op_type)
        else:
            logger.info('COMMAND Invalid options')
            self.print_help()
        logger.info('COMMAND END sync packageversion')

    def get_package(self, options):
        if options['package_name']:
            return Package.objects.get(package_name=options['package_name'])
        elif options['package_id']:
            return Package.objects.get(pk=options['package_id'])
        else:
            return None

    def get_packageversion(self, options, package):
        if package and options['version_name']:
            return package.versions.get(package_name=options['package_name'])
        elif package and options['version_code']:
            return package.versions.get(version_code=options['version_code'])
        elif package:
            return package.versions.latest_published()
        elif options['version_id']:
            return PackageVersion.objects.get(pk=options['version_id'])
        else:
            raise Exception('Invalid Options for packageversion query')

    def get_random_versions(self, options):
        limit = options['limit']
        return PackageVersion.objects.published().order_by('?')[0:limit]

    def sync_processor(self, version, op_type):
        package = version.package
        logger.info('start sync process')
        logger.info(dict(package_name=package.package_name,
                         version_name=version.version_name))
        processor = version.sync_processor_class(version)
        op_method = getattr(processor, op_type)
        flag, results, faileds = op_method()
        logger.info("result: %s, all:%s, fail: %s" %
                    (flag, len(results), len(faileds)))
        logger.info('end sync process')

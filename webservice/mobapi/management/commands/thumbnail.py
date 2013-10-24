# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from easy_thumbnails.files import generate_all_aliases
from easy_thumbnails.exceptions import InvalidImageFormatError
from optparse import make_option
from warehouse.models import (PackageVersion,
                              PackageVersionScreenshot)
from taxonomy.models import Category, Topic
from promotion.models import Advertisement

class Command(BaseCommand):

    models = {
        'warehouse.PackageVersionScreenshot': PackageVersionScreenshot,
        'warehouse.PackageVersion': PackageVersion,
        'taxonomy.Category': Category,
        'taxonomy.Topic': Topic,
        'promotion.Advertisement': Advertisement
    }

    help = 'generate thumbnails for model field, ' \
           'model such as warehouse.models.PackageVersion'

    option_list = BaseCommand.option_list + (
        make_option('--sizealias',
                    action='store', dest='sizealias', default='all',
                    help='size alias of settings.THUMBNAIL_ALIASES'),
        make_option('--field',
                    action='store', dest='field', default='all',
                    help='ThumbnailerImageField name of model, '
                         'such as icon'),
    )

    def handle(self, *args, **options):
        fields = self.validate_option_field(options.get('field'))
        for name, klass in self.models.items():
            self.generate_model_thumbnails_for_fields(klass, fields)

    def validate_option_field(self, option):
        tbfields = ('icon', 'cover', 'image')
        fields = ()
        if option == 'all':
            fields = tbfields
        elif option in tbfields:
            fields = (option, )
        else:
            raise CommandError('field option wrong')

        return fields

    def generate_model_thumbnails_for_fields(self, model, fields):
        objs = model.objects.all()
        for o in objs:
            self.generate_object_thumbnails_for_fields(o, fields)

    def generate_object_thumbnails_for_fields(self, obj, fields):
        for f in fields:
            if hasattr(obj, f) and getattr(obj, f) and getattr(obj, f)._file:
                try:
                    generate_all_aliases(getattr(obj, f), include_global=True)
                except InvalidImageFormatError as e:
                    print(e)



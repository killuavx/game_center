# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions
from warehouse.models import Package
from django.utils.translation import ugettext_lazy as _


class PackageTranslationOptions(TranslationOptions):
    fields = ('title', )
    fallback_values = _('-- sorry, no translation provided --')

translator.register(Package, PackageTranslationOptions)
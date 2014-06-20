# -*- coding: utf-8 -*-
import io
from django.conf import settings
from django.db.models import FloatField, IntegerField, CharField
from mezzanine.generic.fields import (
    BaseGenericRelation)
from toolkit.helpers import file_md5
from django.db.models import FileField as DFileField
from mezzanine.core.fields import FileField


def update_pkgfile_meta(instance, fieldname):
    from toolkit.fields import file_md5
    import io
    file_field = getattr(instance, fieldname)
    if file_field:
        with io.FileIO(file_field.path) as f:
            setattr(instance, '%s_md5' % fieldname, file_md5(f))
        setattr(instance, '%s_size' % fieldname, file_field.size)
        return instance
    return None


class StarsField(BaseGenericRelation):

    related_model = "toolkit.Star"
    fields = {"%s_count": IntegerField(verbose_name='Count', default=0, editable=False),
              "%s_sum": IntegerField(verbose_name='Sum', default=0, editable=False),
              "%s_average": FloatField(verbose_name='Average', default=0, editable=False),

              "%s_good_count": IntegerField(verbose_name='Good Count', default=0, editable=False),
              "%s_good_rate": FloatField(verbose_name='Good Rate', default=0, editable=False),
              "%s_medium_count": IntegerField(verbose_name='Medium Count', default=0, editable=False),
              "%s_medium_rate": FloatField(verbose_name='Medium Rate', default=0, editable=False),
              "%s_low_count": IntegerField(verbose_name='Low Count', default=0, editable=False),
              "%s_low_rate": FloatField(verbose_name='Low Rate', default=0, editable=False),
    }

    def related_items_changed(self, instance, related_manager):
        """
        Calculates and saves the rating.
        """
        ratings = [r.value for r in related_manager.all()]
        instance = self._calc_base_value(instance, ratings)
        instance = self._calc_good_value(instance, ratings)
        instance = self._calc_medium_value(instance, ratings)
        instance = self._calc_low_value(instance, ratings)
        instance.save()

    def _calc_base_value(self, instance, ratings):
        count = len(ratings)
        _sum = sum(ratings)
        average = _sum / count if count > 0 else 0
        setattr(instance, "%s_count" % self.related_field_name, count)
        setattr(instance, "%s_sum" % self.related_field_name, _sum)
        setattr(instance, "%s_average" % self.related_field_name, average)
        return instance

    def _calc_good_value(self, instance, ratings):
        """
            good: star 4-5
                good_count = count(value in 4,5)
                good_rate = good_count / count(all)
        """
        _count, _rate = self.__calc_count_rate(instance, ratings, values=(4, 5))
        setattr(instance, "%s_good_count" % self.related_field_name, _count)
        setattr(instance, "%s_good_rate" % self.related_field_name, _rate)
        return instance

    def _calc_medium_value(self, instance, ratings):
        """
            medium: star 2-3
                medium_count = count(value in 2,3) / count(all)
                medium_rate = count(value in 2,3) / count(all)
        """
        _count, _rate = self.__calc_count_rate(instance, ratings, values=(2, 3))
        setattr(instance, "%s_medium_count" % self.related_field_name, _count)
        setattr(instance, "%s_medium_rate" % self.related_field_name, _rate)
        return instance

    def _calc_low_value(self, instance, ratings):
        """
            low: star 1
                low_count = count(value == 1)
                low_rate = low_count / count(all)
        """
        _count, _rate = self.__calc_count_rate(instance, ratings, values=(1,))
        setattr(instance, "%s_low_count" % self.related_field_name, _count)
        setattr(instance, "%s_low_rate" % self.related_field_name, _rate)
        return instance

    def __calc_count_rate(self, instance, ratings, values):
        vals_count = len(list(filter(lambda v: v in values, ratings)))
        all_count = getattr(instance, "%s_count" % self.related_field_name)
        rate = vals_count / all_count if all_count > 0 else 0
        return vals_count, rate


class FileWithMetaField(DFileField):

    def __init__(self, *args, **kwargs):
        super(FileWithMetaField, self).__init__(*args, **kwargs)
        self.added_fields = self._get_added_fields()

    def _get_added_fields(self):
        return {
            "size": ('%s_size', IntegerField(default=0,
                                             blank=True,
                                             editable=False)),
            "md5": ('%s_md5', CharField(default=None,
                                        null=True,
                                        blank=True,
                                        max_length=40,
                                        editable=False)),
        }

    def _field_name(self, attrname, name):
        return self.added_fields[name][0] % attrname

    def _field_type(self, name):
        return self.added_fields[name][1]

    def contribute_to_class(self, cls, name):
        if not cls._meta.abstract:
            for idx in self.added_fields.keys():
                cls.add_to_class(self._field_name(name, idx), self._field_type(idx))
        super(FileWithMetaField, self).contribute_to_class(cls, name)

    def pre_save(self, model_instance, add):
        file = getattr(model_instance, self.attname)
        update_flag = False
        if file and not file._committed:
            update_flag = True
        file = super(FileWithMetaField, self).pre_save(model_instance, add)

        if update_flag:
            _file_size = file.size
            with io.FileIO(file.path) as f:
                _md5_text = file_md5(f)
            setattr(model_instance, self._field_name(self.attname, 'size'), _file_size)
            setattr(model_instance, self._field_name(self.attname, 'md5'), _md5_text)
        elif not file:
            setattr(model_instance, self._field_name(self.attname, 'size'), 0)
            setattr(model_instance, self._field_name(self.attname, 'md5'), None)
        return file


class PkgFileField(FileWithMetaField):

    def pre_save(self, model_instance, add):
        fileattr = getattr(model_instance, self.attname)
        tracker = getattr(model_instance, 'tracker', None)
        changed = tracker and tracker.has_changed(self.attname)
        if changed and fileattr and hasattr(fileattr.storage, 'remote_size') \
            and hasattr(fileattr.storage, 'is_qiniu_file') \
            and fileattr.storage.is_qiniu_file(fileattr.name):
            try:
                _file_size = fileattr.storage.remote_size(fileattr.name)
                setattr(model_instance,
                        self._field_name(self.attname, 'size'),
                        _file_size)
                setattr(model_instance,
                        self._field_name(self.attname, 'md5'), '')
                return fileattr
            except FileNotFoundError:
                raise
        else:
            return super(FileWithMetaField, self).pre_save(model_instance, add)


class MultiResourceField(BaseGenericRelation):

    related_model = "toolkit.Resource"
    fields = {
        '%s_count': IntegerField(default=0, blank=True, editable=False),
    }

    def related_items_changed(self, instance, related_manager):
        resources = related_manager.all()
        count_field = '%s_count' % self.related_field_name
        setattr(instance, count_field, resources.count())
        # set to call cdn sync action
        instance._sync_files = True
        instance.save()

# South requires custom fields to be given "rules".
# See http://south.aeracode.org/docs/customfields.html
if "south" in settings.INSTALLED_APPS:
    try:
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules(rules=[
            ((BaseGenericRelation,), [], {}),
            ((FileWithMetaField,), [], {})
        ],
                                patterns=["toolkit\.fields\."])
    except ImportError:
        pass


from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails import files
from toolkit.storage import package_storage, QiniuPackageFileStorage
from easy_thumbnails.alias import aliases
from django.db.models.fields.files import ImageFieldFile
from easy_thumbnails.files import FakeField, FakeInstance


class QiniuImageStorage(QiniuPackageFileStorage):

    def __init__(self, options, *args, **kwargs):
        self.options = options
        super(QiniuImageStorage, self).__init__(*args, **kwargs)

    def url(self, name):
        url = super(QiniuImageStorage, self).url(name)
        w, h = self.options['size']
        imgformat = self.options.get('format', 'jpg')
        return url + "?imageMogr2/thumbnail/%sx%s/format/%s" % (w, h, imgformat)


class QiniuThumbnailerImageFieldFile(files.ThumbnailerFieldFile):

    def imageMogr2FieldFile(self, options):
        fake_field = FakeField(storage=QiniuImageStorage(options=options))
        instance = FakeInstance()
        return ImageFieldFile(instance, name=self.name, field=fake_field)

    def __getitem__(self, alias):
        if self.storage.is_qiniu_file(self.name):
            options = aliases.get(alias, target=self.alias_target)
            return self.imageMogr2FieldFile(options)
        return super(QiniuThumbnailerImageFieldFile, self).__getitem__(alias)


class QiniuThumbnailerImageField(ThumbnailerImageField):

    attr_class = QiniuThumbnailerImageFieldFile

    def __init__(self, *args, **kwargs):
        storage = kwargs.pop('storage', None) or package_storage
        thumbnail_storage = kwargs.pop('thumbnail_storage', None) or package_storage
        super(QiniuThumbnailerImageField, self)\
            .__init__(storage=storage,
                      thumbnail_storage=thumbnail_storage,
                      *args, **kwargs)

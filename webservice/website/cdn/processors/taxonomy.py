# -*- coding: utf-8 -*-
from os.path import dirname
from website.cdn.errors import WorkingDirectoryNotFound
from .base import ModelProcessor


class TaxonomyProcessor(ModelProcessor):

    def __init__(self, instance):
        super(TaxonomyProcessor, self).__init__(instance)
        self.relative_path = self.get_relative_working_path()

    def get_relative_working_path(self):
        file_not_found = None
        path = None
        try:
            self.instance.icon.size
            path = self.instance.icon.path
        except (ValueError, FileNotFoundError) as e1:
            file_not_found = e1
            if hasattr(self.instance, 'cover'):
                try:
                    self.instance.cover.size
                    path = self.instance.cover.path
                    file_not_found = None
                except (ValueError, FileNotFoundError) as e2:
                    file_not_found = e2

        if file_not_found:
            raise WorkingDirectoryNotFound(
                "working direcotry %s '%s' not found" % (self.instance, path))

        return dirname(path)


class TopicProcessor(TaxonomyProcessor):
    pass


class CategoryProcessor(TaxonomyProcessor):
    pass


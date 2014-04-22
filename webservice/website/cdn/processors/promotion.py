# -*- coding: utf-8 -*-
from os.path import dirname
from website.cdn.errors import WorkingDirectoryNotFound
from .base import ModelProcessor


class AdvertisementProcessor(ModelProcessor):

    def __init__(self, instance):
        super(AdvertisementProcessor, self).__init__(instance)
        self.relative_path = self.get_relative_working_path()

    def get_relative_working_path(self):
        try:
            self.instance.cover.size
        except FileNotFoundError:
            path = self.instance.cover.path
            raise WorkingDirectoryNotFound(
                "working direcotry %s '%s' not found" % (self.instance, path))
        except ValueError:
            raise WorkingDirectoryNotFound(
                "working direcotry %s not found" % self.instance)
        return dirname(self.instance.cover.name)

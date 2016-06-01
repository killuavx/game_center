# -*- coding: utf-8 -*-
from os.path import dirname
from website.cdn.errors import WorkingDirectoryNotFound
from .base import ModelProcessor


class ClientPackageVersionProcessor(ModelProcessor):

    def __init__(self, instance):
        super(ClientPackageVersionProcessor, self).__init__(instance)
        self.relative_path = self.get_relative_working_path()

    def get_relative_working_path(self):
        try:
            self.instance.download.url
        except FileNotFoundError:
            path = self.instance.download.path
            raise WorkingDirectoryNotFound(
                "working direcotry %s '%s' not found" % (self.instance, path))
        except ValueError:
            raise WorkingDirectoryNotFound(
                "working direcotry %s not found" % self.instance)
        return dirname(self.instance.download.path)


class LoadingCoverProcessor(ModelProcessor):

    def __init__(self, instance):
        super(LoadingCoverProcessor, self).__init__(instance)
        self.relative_path = self.get_relative_working_path()

    def get_relative_working_path(self):
        try:
            self.instance.image.url
        except FileNotFoundError:
            raise WorkingDirectoryNotFound(
                "working direcotry %s not found" % self.instance)
        return dirname(self.instance.image.path)

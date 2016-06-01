# -*- coding: utf-8 -*-
from os.path import dirname
from website.cdn.errors import WorkingDirectoryNotFound
from .base import ModelProcessor


class ProfileProcessor(ModelProcessor):

    def __init__(self, instance):
        super(ProfileProcessor, self).__init__(instance)
        self.relative_path = self.get_relative_working_path()

    def get_relative_working_path(self):
        try:
            self.instance.icon.size
        except FileNotFoundError:
            path = self.instance.icon.path
            raise WorkingDirectoryNotFound(
                "working direcotry %s '%s' not found" % (self.instance, path))
        return dirname(self.instance.icon.name)

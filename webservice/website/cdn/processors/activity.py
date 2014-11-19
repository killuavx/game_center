# -*- coding: utf-8 -*-
from website.cdn.errors import WorkingDirectoryNotFound
from .base import ModelProcessor


class ActivityProcessor(ModelProcessor):

    def __init__(self, instance):
        super(ActivityProcessor, self).__init__(instance)
        self.relative_path = self.get_relative_working_path()

    def get_relative_working_path(self):
        if self.instance.workspace:
            return str(self.instance.workspace)
        raise WorkingDirectoryNotFound(
            "Activity %s working direcotry not found" % self.instance)

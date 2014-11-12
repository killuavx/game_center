# -*- coding: utf-8 -*-
from django.core.files.uploadhandler import MemoryFileUploadHandler


class MemoryFileUploadExceptVideoHandler(MemoryFileUploadHandler):

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        if self.request and "video" in self.request.path:
            self.activated = False
            return
        super(MemoryFileUploadExceptVideoHandler, self)\
            .handle_raw_input(input_data=input_data,
                              META=META,
                              content_length=content_length,
                              boundary=boundary,
                              encoding=encoding)

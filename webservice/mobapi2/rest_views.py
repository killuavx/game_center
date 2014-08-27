# -*- coding: utf-8 -*-

from rest_framework import serializers
from mobapi2.serializers import NotePaginationSerializer
from rest_framework.reverse import reverse


class NotePaginationAPIViewMixin(object):

    pagination_serializer_class = NotePaginationSerializer

    def get_note_slug(self):
        raise NotImplementedError

    def get_pagination_serializer(self, page):
        """
        Return a serializer instance to use with paginated data.
        """
        note_view_name = 'note-detail'
        this = self

        class NoteSerializerClass(self.pagination_serializer_class):

            def get_note_url(self, obj):
                view_name = self.opts.router.get_base_name(note_view_name)
                kwargs = dict()
                kwargs['slug'] = this.get_note_slug()
                request = self.context.get('request', None)
                format = self.context.get('format', None)
                return reverse(view_name,
                               kwargs=kwargs,
                               request=request,
                               format=format)

            class Meta:
                object_serializer_class = self.get_serializer_class()

        pagination_serializer_class = NoteSerializerClass
        context = self.get_serializer_context()
        return pagination_serializer_class(instance=page, context=context)



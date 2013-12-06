# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import mixins
from analysis.serializers import EventSerializer
from analysis.documents.event import Event
from mobapi.authentications import PlayerTokenAuthentication


class EventViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):

    model = Event
    queryset = Event.objects
    serializer_class = EventSerializer
    permission_classes = ()
    authentication_classes = (PlayerTokenAuthentication, )

    def get_serializer(self, instance=None, data=None,
                       files=None, many=False, partial=False):
        if instance is None and data:
            instance = self.model(**data)
        serializer = super(EventViewSet, self).get_serializer(instance=instance,
                                                              data=data,
                                                              files=files,
                                                              many=many,
                                                              partial=partial)
        request = serializer.context.get('request')
        if request:
            serializer.object.user_pk = request.user.pk
        return serializer


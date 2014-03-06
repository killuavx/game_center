# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context, RequestContext
from django_widgets.loading import registry as widget_registry


class WidgetHttpResponse(HttpResponse):

    def __init__(self, request, widget_name='', context=dict(), *args, **kwargs):
        self.context_data = context
        self.request = request
        self.current_app = kwargs.get('app')
        self.widget_name = widget_name
        super(WidgetHttpResponse, self)\
            .__init__(content=self.render_widget_content(), *args, **kwargs)

    def resolve_context(self, context):
        if isinstance(context, Context):
            return context
        return RequestContext(self.request, context, current_app=self.current_app)

    def resolve_widget(self, widget_name):
        return widget_registry.get(widget_name)

    def render_widget_content(self):
        context = self.resolve_context(self.context_data)
        widget = self.resolve_widget(self.widget_name)
        return widget.render(context, None, self.context_data)


class WidgetCacheHttpResponse(WidgetHttpResponse):
    pass
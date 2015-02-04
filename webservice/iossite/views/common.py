# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.template import RequestContext
from django.template.loader import get_template
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def page_not_found(request, template_name="iossite/errors/404.html"):
    """
    Mimics Django's 404 handler but with a different template path.
    """
    context = RequestContext(request, {
        "STATIC_URL": settings.STATIC_URL,
        "request_path": request.path,
        })
    t = get_template(template_name)
    return HttpResponseNotFound(t.render(context))


@requires_csrf_token
def server_error(request, template_name="iossite/errors/500.html"):
    """
    Mimics Django's error handler but adds ``STATIC_URL`` to the
    context.
    """
    context = RequestContext(request, {"STATIC_URL": settings.STATIC_URL})
    t = get_template(template_name)
    return HttpResponseServerError(t.render(context))

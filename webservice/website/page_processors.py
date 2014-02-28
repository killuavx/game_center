# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve, Resolver404
from django.http import Http404
from mezzanine.pages.page_processors import processor_for
from taxonomy.models import Category
from mezzanine.conf import settings


categories_page_slug = 'categories'
@processor_for(categories_page_slug)
def categories_fill(request, page):
    category = None
    if request.method == "GET":
        try:
            func, args, kwargs = resolve(request.path_info)
            # mezzine.pages.views.page contains kwargs['slug']
            # with value "categories", replace it to default category slug
            category_slug = kwargs.get('slug')
            if categories_page_slug == category_slug:
                category_slug = settings.GC_CATEGORIES_DEFAULT_SLUG
            category = Category.objects.get(slug=category_slug)
        except (Resolver404, Category.DoesNotExist) as e:
            raise Http404()
    return {"category": category}

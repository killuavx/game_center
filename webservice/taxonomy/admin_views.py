# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

from taxonomy.models import Category

@staff_member_required
def tree(request):
    return render_to_response(
        "admin/category/tree.html",
        {'categories' : Category.objects.filter(parent=None)},
        RequestContext(request, {}),
    )
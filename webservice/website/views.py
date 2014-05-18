# -*- coding: utf-8 -*-
from os.path import splitext
from urllib.parse import urlsplit
from mezzanine.conf import settings
from django.core.paginator import EmptyPage, Paginator

from django.http import Http404, HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import resolve

from .response import WidgetHttpResponse
from toolkit.helpers import get_client_event_data
from warehouse.models import PackageVersion, Package
from analysis.documents.event import Event
from website.models import get_package_by_package_name, get_packageversion_by_package
from website.models import get_root_category_slug_by_package, get_all_categories, get_leaf_categories
from website.models import filter_packages_by_category_slug, get_all_packages, get_authors_by_topic
from website.models import is_topic_slug, get_topic_slug, get_topic_by_slug, filter_packages_by_topic
from website.models import paginize_items, get_supported_language, filter_packages_by_supported_language
from website.models import get_category_slug, get_all_sub_cats, get_all_collections, get_packages_by_topic


def _download_packageversion_response(packageversion, filetype):
    try:
        download_url = packageversion.get_download_static_url(filetype=filetype)
    except (AttributeError, ValueError):
        raise Http404()
    # counter plus one
    # from website.tasks import packageversion_download_counter
    #### website/tasks.py
    # from analysis.documents.fields import DownloadCounter
    # pv.download_counter\
    #                 .add(DownloadCounter(user=request.user,
    #                                      packageversion=pv.pk,
    #                                      filetype=filetype))
    response = redirect(download_url)
    # 重命名会导致重定向失败，使得cdn地址失效
    """
    new_filename = "%s-%s%s" % (packageversion.package.package_name,
                                packageversion.version_name,
                                splitext(download_url)[-1])
    response['Content-Disposition'] = 'attachment; filename=%s' % new_filename
    bits = urlsplit(download_url)
    path = bits[2]
    response['X-Accel-Redirect'] = "%s?renameto=%s" %(path, new_filename)
    """
    return response

def _is_breakpoint_continual_download(request):
    """
        是否断点续传
    """
    request_range = request.META.get('HTTP_RANGE', None)
    if request_range is None:
        return False

    bytes_bits = request_range.strip('bytes=').split('-')
    if str(bytes_bits[0]).isnumeric() and int(bytes_bits[0]) == 0:
        return False

    return True

def _download_make_event(request, response, packageversion, filetype=None):
    """
        下载事件的日志记录
    """
    if _is_breakpoint_continual_download(request):
        return None

    kwargs = get_client_event_data(request)
    entrytype = kwargs.get('entrytype', request.GET.get('entrytype', 'web'))
    imei = kwargs.get('imei', request.GET.get('imei', ''))
    user = request.user

    event = Event(**kwargs)
    event.imei = imei
    event.eventtype = 'download'
    event.entrytype = entrytype
    event.file_type = filetype
    event.domain = request.get_host()
    if hasattr(request, 'get_client_ip'):
        event.client_ip = request.get_client_ip()

    event.download_package_name = packageversion.package.package_name
    event.download_version_name = packageversion.version_name

    event.current_uri = request.build_absolute_uri()
    event.redirect_to = response.get('Location')
    event.referer = request.META.get('HTTP_REFERER')
    event.user = user
    event.save()
    return event


def download_package(request, package_name, version_name=None,
                     filetype=None, *args, **kwargs):
    try:
        qs = PackageVersion.objects\
            .filter(package__package_name=package_name).published()
        if version_name:
            qs = qs.filter(version_name=version_name)
        packageversion = qs.get()
    except (PackageVersion.DoesNotExist, PackageVersion.MultipleObjectsReturned):
        raise Http404()

    response = _download_packageversion_response(packageversion, filetype)
    try:
        event = _download_make_event(request, response, packageversion, filetype)
    except Exception as e:
        pass
    return response


def download_packageversion(request, pk, filetype=None, *args, **kwargs):
    try:
        packageversion = PackageVersion.objects.published().get(pk=pk)
    except PackageVersion.DoesNotExist:
        raise Http404()

    response = _download_packageversion_response(packageversion, filetype)
    try:
        event = _download_make_event(request, response, packageversion, filetype)
    except Exception as e:
        pass
    return response


def packageversion_detail(request, package_name, version_name=False,
                          template='pages/packages/version-detail.html',
                          *args, **kwargs):
    if version_name is False:
        try:
            package = Package.objects.published().get(package_name=package_name)
        except Package.DoesNotExist:
            raise Http404
        version = package.versions.latest_publish()
    else:
        try:
            version = PackageVersion.objects.published()\
                .get(package__package_name=package_name, version_name=version_name)
        except PackageVersion.DoesNotExist:
            raise Http404()
        package = version.package

    return TemplateResponse(request=request, template=template, context=dict(
        package=package,
        version=version,
        package_name=package_name,
        version_name=version_name,
    ))


def category_package_list(request, slug=settings.GC_CATEGORIES_DEFAULT_SLUG,
                          template='pages/categories.html', *args, **kwargs):
    context = dict(
        slug=slug,
        ordering=request.GET.get('ordering'),
        page_num=request.GET.get('page'),
    )
    if request.is_ajax() or request.GET.get('ajax'):
        response = WidgetHttpResponse(request=request,
                                      context=context,
                                      widget_name='CategoryPackageListWidget')
        return response

    return TemplateResponse(request=request, template=template, context=context)


def masterpiece_view(request, template='pages/masterpiece.html', *args, **kwargs):
    context = dict(
        page_num=request.GET.get('page'),
    )
    if request.is_ajax() or request.GET.get('ajax'):
        response = WidgetHttpResponse(request=request,
                                      context=context,
                                      widget_name='MasterpiecePackageListWidget')
        return response

    return TemplateResponse(request=request, template=template, context=context)


def topics_view(request, template='pages/topics.html',
                *args, **kwargs):
    context = dict(
        page_num=request.GET.get('page'),
    )
    if request.is_ajax() or request.GET.get('ajax'):
        try:
            response = WidgetHttpResponse(request=request,
                                          context=context,
                                          widget_name='TopicsTopicListWidget')
            return response
        except Exception as e:
            raise Http404()
    return TemplateResponse(request=request, template=template, context=context)


def topic_package_list(request, slug, template='pages/topics/detail.html',
                       *args, **kwargs):
    context = dict(
        slug=slug,
        page_num=request.GET.get('page'),
    )
    if request.is_ajax() or request.GET.get('ajax'):
        try:
            response = WidgetHttpResponse(request=request,
                                          context=context,
                                          widget_name='TopicsPackageListWidget')
        except EmptyPage:
            raise Http404()
        return response

    return TemplateResponse(request=request, template=template, context=context)



@csrf_exempt
def cdn_feedback(request, slug, *args, **kwargs):
    from website.cdn.core import Feedback
    from website.cdn.parsers import OperationResponse
    ctx1 = request.GET.get('context')
    ctx2 = request.POST.get('context')
    if not(ctx1 or ctx2) or slug != 'ccsc':
        response = OperationResponse(OperationResponse.STATUS_CODE_FAILED,
                                     'Bad Requeset')
        return HttpResponseBadRequest(response.render(),
                                      mimetype='text/xml; charset=utf-8')
    context = ctx1 or ctx2
    feedback = Feedback()
    response = feedback.process(content=context)
    return HttpResponse(response.render(),
                        mimetype='text/xml; charset=utf-8')


def iospc_package_detail_views(request, package_name, *args, **kwargs):
    template = 'iospc/package-detail.html'

    context = {}
    pkg = get_package_by_package_name(package_name)
    all_cats = get_all_categories(pkg)
    leaf_cats = get_leaf_categories(all_cats)
    #print (cats)
    #print (cats)
    context['pkgver'] =  get_packageversion_by_package(pkg)
    context['slug'] = get_root_category_slug_by_package(pkg)
    context['cats'] = leaf_cats

    return TemplateResponse(request=request, template=template, context=context)


def iospc_packages_cat_list_views(request, slug, *args, **kwargs):
    template = 'iospc/categorized-packages-list.html'
    all_packages = get_all_packages()
    packages = filter_packages_by_category_slug(all_packages, slug)
    category_slug, category_query = get_category_slug(request)
    if category_slug != False:
        packages = filter_packages_by_category_slug(packages, category_slug)
    pkgs, page_query = paginize_items(request, packages)

    sub_cats = get_all_sub_cats(slug)

    context = {
        'items': pkgs,
        'slug': slug,
        'cats': sub_cats,
        'page_query': page_query,
        'category_query': category_query
    }

    return TemplateResponse(request=request, template=template, context=context)


def iospc_packages_topic_list_views(request, cat_slug, other_slug, *args, **kwargs):
    template = 'iospc/categorized-packages-list.html'
    all_packages = get_all_packages()
    cat_packages = filter_packages_by_category_slug(all_packages, cat_slug)

    print (other_slug)
    if is_topic_slug(other_slug):
        topic_slug = get_topic_slug(other_slug, cat_slug)
        topic = get_topic_by_slug(topic_slug)
        packages = filter_packages_by_topic(cat_packages, topic)
    elif other_slug == 'latest':
        packages = cat_packages.by_published_order()
    else:
        lang = get_supported_language(other_slug)
        #print (lang)
        if lang:
            packages = filter_packages_by_supported_language(cat_packages, lang)
        else:
            packages = cat_packages

    sub_cats = get_all_sub_cats(cat_slug)
    pkgs, page_query = paginize_items(request, packages)
    context = {
        'items': pkgs,
        'cats': sub_cats,
        'slug': cat_slug,
        'other_slug': other_slug,
        'page_query': page_query,
    }

    return TemplateResponse(request=request, template=template, context=context)


def iospc_packages_collectios_list_views(request, *args, **kwargs):

    template = 'iospc/collections-packages-list.html'

    collections = get_all_collections()

    result = []
    for collection in collections:
        packages = get_packages_by_topic(collection)
        result.append({
            'collection': collection,
            'packages': packages,
        })

    items, page_query = paginize_items(request, result, 2)

    context = {
        'items': items,
        'page_query': page_query,
    }

    return TemplateResponse(request=request, template=template, context=context)



def iospc_collection_detail_views(request, slug, *args, **kwargs):

    template = 'iospc/collection-packages.html'
    packages = []
    collection = get_topic_by_slug(slug)
    if collection:
        packages = get_packages_by_topic(collection)

    context = {
        'collection': collection,
        'packages': packages,
    }

    if slug == 'topic-xiaomo' and 'iospc_masterpiece_packages' \
            == resolve(request.path_info).url_name: # for masterpiece
        items, page_query = paginize_items(request, packages, 2)
        template = 'iospc/masterpiece-packages.html'
        context =  {
            'items': items,
            'page_query': page_query,
        }
    return TemplateResponse(request=request, template=template, context=context)


def iospc_vendors_list_views(request, slug, pk, *args, **kwargs):
    template = 'iospc/vendors-packages.html'

    vendors = []
    current_vendor = None
    topic = get_topic_by_slug(slug)
    if topic:
        vendors = get_authors_by_topic(topic)
        #print (vendors.count())
        if vendors and pk:
            try:
                current_vendor = vendors.get(pk=pk)
            except:
                pass

    if vendors and current_vendor is None:
        current_vendor = vendors[0]

    packages = current_vendor.packages.published()
    items, page_query = paginize_items(request, packages, 1)

    #print (len(items))
    context = {
        'current_vendor': current_vendor,
        'items': items,
        'vendors': vendors,
        'page_query': page_query,
    }

    return TemplateResponse(request=request, template=template, context=context)

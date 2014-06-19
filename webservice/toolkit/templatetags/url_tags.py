# -*- coding: utf-8 -*-
"""qurl is a tag to append, remove or replace query string parameters from an url (preserve order)"""

import re
from django.core.exceptions import ObjectDoesNotExist
from django.template import Library, Node, TemplateSyntaxError
from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode
from django.utils.encoding import smart_str
from toolkit import helpers


register = Library()


@register.tag
def qurl(parser, token):
    """
    Append, remove or replace query string parameters from an url (preserve order)

        {% qurl url [param]* [as <var_name>] %}

    param:
            name=value: replace all values of name by one value
            name=None: remove all values of name
            name+=value: append a new value for name
            name-=value: remove the value of name with the value

    Example::

        {% qurl '/search?page=1&color=blue&color=green' order='name' page=None color+='red' color-='green' %}
        Output: /search?color=blue&order=name&color=red

        {% qurl request.get_full_path order='name' %}
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument (url)" % bits[0])

    url = parser.compile_filter(bits[1])

    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    qs = []
    if len(bits):
        kwarg_re = re.compile(r"(\w+)(\-=|\+=|=)(.*)")
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to url tag")
            name, op, value = match.groups()
            qs.append((name, op, parser.compile_filter(value),))

    return QURLNode(url, qs, asvar)


class QURLNode(Node):
    """Implements the actions of the qurl tag."""

    def __init__(self, url, qs, asvar):
        self.url = url
        self.qs = qs
        self.asvar = asvar

    def render(self, context):
        urlp = list(urlparse(self.url.resolve(context)))
        qp = parse_qsl(urlp[4])
        for name, op, value in self.qs:
            name = smart_str(name)
            value = value.resolve(context)
            value = smart_str(value) if value is not None else None
            if op == '+=':
                qp = list(filter(lambda nv: not(nv[0] == name and nv[1] == value), qp))
                qp.append((name, value,))
            elif op == '-=':
                qp = list(filter(lambda nv: not(nv[0] == name and nv[1] == value), qp))
            elif op == '=':
                qp = list(filter(lambda nv: not(nv[0] == name), qp))
                if value is not None:
                    qp.append((name, value,))

        urlp[4] = urlencode(qp, True)
        url = urlunparse(urlp)

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url

from urllib.parse import urlsplit


def url_has_host(url):
    r = urlsplit(url)
    if r.scheme and r.netloc:
        return True
    return False


def absolute_url(context, inst, abs=True, **kwargs):
    if not inst:
        return ''
    product = kwargs.pop('product', None)
    get_url_as = getattr(inst, 'get_absolute_url_as')
    url = get_url_as(product, **kwargs)

    request = context.get('request')
    site = helpers.get_global_site()
    if site is None and abs and not url_has_host(url):
        if request:
            return request.build_absolute_uri(url)
    return helpers.build_site_absolute_uri(site, url)

register.assignment_tag(absolute_url, takes_context=True, name='absolute_url_as')
register.simple_tag(absolute_url, takes_context=True)


def download_url(context, pv, **kwargs):
    entrytype = None
    if 'product' in kwargs:
        entrytype = kwargs.pop('product')

    url = pv.get_download_url(entrytype=entrytype, **kwargs)
    request = context.get('request')
    if request:
        return request.build_absolute_uri(url)
    return url

register.assignment_tag(download_url, takes_context=True, name='download_url_as')
register.simple_tag(download_url, takes_context=True)

from django.db import models


def resource_url(inst_or_resources, kind='cover', alias='default', size_alias=None):
    if (alias == 'default' or size_alias) and kind in ('cover', 'icon'):
        try:
            fileattr = getattr(inst_or_resources, kind)
            if size_alias:
                return fileattr[size_alias].url
            return fileattr.url
        except (ValueError, AttributeError):
            pass

    if isinstance(inst_or_resources, models.Model):
        try:
            resources = getattr(inst_or_resources, 'resources')
            res = getattr(resources, kind)[alias]
            return res.file.url
        except:
            pass

    if hasattr(inst_or_resources, 'model') and inst_or_resources.model:
        try:
            res = getattr(inst_or_resources, kind)[alias]
            return res.file.url
        except ObjectDoesNotExist:
            pass

    if kind in ('cover', 'icon') and isinstance(inst_or_resources, models.Model):
        try:
            return getattr(inst_or_resources, kind).url
        except (ValueError, AttributeError):
            pass

    return ''

register.assignment_tag(resource_url, name='resource_url_as')
register.simple_tag(resource_url)

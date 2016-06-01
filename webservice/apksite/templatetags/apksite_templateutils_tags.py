
from template_utils.templatetags.templateutils_tags import *

@register.simple_tag
def active_url(request, url_name, **kwargs):
    """
    Returns a class to be assiged CSS styling that should make the chosen
    element highlighted as responsible of being in the active url.

    Usage: Assuming that the reversed url is the current url, this tag will act
    as follows:

    {% active_url request url_name %} -> class="ui-active-url"
    {% active_url request url_name class_name=myclass %} -> class="myclass"
    {% active_url request url_name use_class=False %} -> ui-active-url
    {% active_url request url_name class_name=myclass use_class=False %} -> myclass

    Where "urlname" is the name of the url to check;
    this must be defined in your `URLCONF`, otherwise it will raise
    a NoReverseMatch Error.
    """
    class_name = kwargs.get('class_name', 'ui-active-url')
    use_class = kwargs.get('use_attr', True)

    url = reverse(url_name)
    if request.path.rstrip('/') == url:
        return (class_name, ' class="%s"' % class_name)[use_class]
    return ''


@register.simple_tag
def current_url(request, url_name):
    """
    Returns the reversed url only if it is NOT the current url.
    Otherwise returns the character "`#`"

    Usage:
    <a href="{% current_url request url_name %}">Some link</a>
    """
    url = reverse(url_name)
    if request.path.rstrip('/') == url:
        return '#'
    return url

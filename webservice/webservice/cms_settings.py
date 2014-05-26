# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from webservice.settings import *
from webservice.module_settings.logging_prd import *
from webservice.module_settings.db_env import *
from webservice.module_settings.mongo_env import *

DEBUG = TEMPLATE_DEBUG = True

HOST_URL = os.getenv('GC_HOST_URL', '')

SITE_TITLE = '虫虫游戏'

# Name of the directory for the project.
PROJECT_DIRNAME = PROJECT_PATH.split(os.sep)[-1]

NEVERCACHE_KEY = "%(NEVERCACHE_KEY)s"

CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME

DEBUG = TEMPLATE_DEBUG = False

SEND_BROKEN_LINK_EMAILS = False

USE_SOUTH = True

USE_I18N = False

MEDIA_URL = HOST_URL.replace('gc', 'media') + MEDIA_URL

STATIC_URL = HOST_URL.replace('gc', 'static') + STATIC_URL

PUBLISH_MEDIA_URL = MEDIA_URL

PUBLISH_STATIC_URL = STATIC_URL

TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS) + [
    'mezzanine.conf.context_processors.settings',
]

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
if 'django.contrib.redirects.middleware.RedirectFallbackMiddleware' in MIDDLEWARE_CLASSES:
    MIDDLEWARE_CLASSES\
        .remove('django.contrib.redirects.middleware.RedirectFallbackMiddleware')
MIDDLEWARE_CLASSES = [
    "mezzanine.core.middleware.UpdateCacheMiddleware",
     ] + MIDDLEWARE_CLASSES + [
    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.RedirectFallbackMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
]

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

#COMMENTS_APP = 'comment'
COMMENTS_DEFAULT_APPROVED = True
COMMENTS_NOTIFICATION_EMAILS = ''
COMMENT_FILTER = None


#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    "debug_toolbar",
    "django_extensions",
    "compressor",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}

PAGE_MENU_TEMPLATES = (
    (1, "Top navigation bar", "pages/menus/header.haml"),
    (2, "Left-hand tree", "pages/menus/tree.html"),
    (3, "Footer", "pages/menus/footer_links.haml"),
    (5, "iOS PC Navigation Menus", "pages/pc/menu/header.haml"),
)

replace_idx = INTERNAL_APPS.index('suit')
INTERNAL_APPS[replace_idx+1:replace_idx+1] = [
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.pages",
    "mezzanine.galleries",
]
INTERNAL_APPS.append('mezzanine.accounts')
INTERNAL_APPS.append('template_utils')
INTERNAL_APPS.pop(replace_idx)
EXTENDAL_APPS.append('website')
INSTALLED_APPS = INTERNAL_APPS + EXTENDAL_APPS

REST_FRAMEWORK.update(dict(
    #DEFAULT_RENDERER_CLASSES=(
    #    'rest_framework.renderers.JSONRenderer',
    #),
))

# Whether to use cache for inline compilation
STATIC_PRECOMPILER_USE_CACHE = False

COMMENTS_NUM_LATEST = 5
COMMENTS_UNAPPROVED_VISIBLE = False
COMMENTS_REMOVED_VISIBLE = False

RICHTEXT_ALLOWED_TAGS = [
    'section', 'input', 'div',
] + [ "a", "abbr", "acronym", "address", "area", "b", "bdo", "big",
        "blockquote", "br", "button", "caption", "center", "cite", "code",
        "col", "colgroup", "dd", "del", "dfn", "dir", "div", "dl", "dt",
        "em", "fieldset", "font", "form", "h1", "h2", "h3", "h4", "h5",
        "h6", "hr", "i", "img", "input", "ins", "kbd", "label", "legend",
        "li", "map", "menu", "ol", "optgroup", "option", "p", "pre", "q",
        "s", "samp", "select", "small", "span", "strike", "strong", "sub",
        "sup", "table", "tbody", "td", "textarea", "tfoot", "th", "thead",
        "tr", "tt", "u", "ul", "var", "wbr",
]

_ = gettext
ADMIN_MENU_ORDER =(
    (_("Content"), ("pages.Page", "blog.BlogPost", "blog.BlogCategory",
                    "generic.ThreadedComment", (_("Media Library"), "fb_browse"),)),
    (_("Site"), ("sites.Site", "redirects.Redirect", "conf.Setting")),
    (_("Account"), ("auth.Group", "auth.User", "auth.Profile", "authtoken.Token")),
    (_("Warehouse"), ("warehouse.Package", "warehouse.PackageVersion", "warehouse.Author")),
    (_("Taxonomy"), ("taxonomy.Category", "taxonomy.Topic", "taxonomy.TopicalItem", "tagging.tag"),),
    (_("Client App"), ("clientapp.ClientPackageVersion", )),
    (_("Promotion"), ("promotion.place", "promotion.Advertisement",)),
    (_("Searcher"), ("searcher.tipsword", )),
    (_("Comment"), ("comment.Comment", )),
)

os.environ['PATH'] = '%s:%s' %('/home/www-data/.nvm/v0.11.9/bin' , os.environ['PATH'])

LESS_EXECUTABLE = '/home/www-data/.nvm/v0.11.9/bin/lessc'

COFFEESCRIPT_EXECUTABLE = \
    '/home/www-data/.nvm/v0.11.9/bin/coffee'


ACCOUNTS_PROFILE_VIEWS_ENABLED = True


FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
    'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv'],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p'],
    'Code': ['.html', '.py', '.js', '.css'],
    'AndroidApp': ['.cpk', '.apk'],
    'iOSApp': ['.ipa'],
}

FILEBROWSER_SELECT_FORMATS = {
    'File': ['Folder', 'Document'],
    'Image': ['Image'],
    'Media': ['Video', 'Audio'],
    'Document': ['Document'],
    # for TinyMCE we can also define lower-case items
    'image': ['Image'],
    'file': ['Folder', 'Image', 'Document'],
    'media': ['Video', 'Audio'],
    'Package': ['iOSApp', 'AndroidApp']
}


FILEBROWSER_DIRECTORY = ''

try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())

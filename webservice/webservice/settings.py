# -*- coding: utf-8 -*-
# Django settings for webservice
from os.path import join, dirname, abspath

gettext = lambda s: s
PROJECT_PATH = abspath(dirname(dirname(__file__)))

#APPEND_SLASH = False

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Ranger.Huang', 'ranger.huang@ccplay.com.cn'),
)


SHORT_DATE_FORMAT = 'm-d'
DATE_FORMAT = 'Y-m-d'
SHORT_DATETIME_FORMAT = 'Y-m-d P'


SEND_BROKEN_LINK_EMAILS = True
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    '*',
    '.ccplay.com.cn',
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-cn'
LANGUAGES_SUPPORTED = ('en', 'zh-cn',)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = join(PROJECT_PATH, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    join(PROJECT_PATH, 'fontend-static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    # for fontend static files precompiler
    'static_precompiler.finders.StaticPrecompilerFinder',
)

# List of enabled compilers
STATIC_PRECOMPILER_COMPILERS = (
    "static_precompiler.compilers.CoffeeScript",
    "static_precompiler.compilers.LESS",
)

# Whether to use cache for inline compilation
STATIC_PRECOMPILER_USE_CACHE = True
# Cache timeout for inline styles (in seconds). Default: 30 days.
# STATIC_PRECOMPILER_CACHE_TIMEOUT =

# Path to CoffeeScript compiler executable
COFFEESCRIPT_EXECUTABLE = 'coffee'

# Path to LESS compiler executable.
LESS_EXECUTABLE = 'lessc'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&bfc%u6_w7)&r$(utbxk#!idnv*3bm^tqnc-lgrwq0=%lh@j7%'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'djaml.loaders.DjamlAppDirectoriesLoader',
        'djaml.loaders.DjamlFilesystemLoader',
    )),
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',

    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'webservice.middlewares.RequestBindRemoteAddrMethodMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'webservice.middlewares.RequestFillLanguageCodeMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'toolkit.middleware.TokenAuthenticationMiddleware',
)

ROOT_URLCONF = 'webservice.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'webservice.wsgi.application'

TEMPLATE_DIRS = (
    join(PROJECT_PATH, 'templates'),
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

INTERNAL_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.redirects',
    'django.contrib.sites',
    "django.contrib.sitemaps",
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.comments',
    'PIL',
    'easy_thumbnails',
    'guardian',
    'south',
    'suit',
    'mptt',
    'reversion',
    'sizefield',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'webservice.Fix_PIL',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'rest_framework_extensions',
    'tagging',
    'tagging_autocomplete',
    'djrill',
    #'djohno',

    'haystack',
    'redis_cache.stats',
    'static_precompiler',
    'django_widgets',
    'url_tools',
    'django_user_agents',
    'memoize',
    'djcelery',
    'import_export',
    'cache_tagging.django_cache_tagging',
]

EXTENDAL_APPS = [
    'toolkit',
    'mobapi',
    'clientapp',
    'searcher',
    'taxonomy',
    'warehouse',
    'promotion',
    'account',
    'comment',
    'analysis',
    'webmob',
    'ranking',
    'mobapi2',
    'crawler',
    'activity',
]
INSTALLED_APPS = INTERNAL_APPS + EXTENDAL_APPS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LANGUAGES = (
    ('cn', gettext('Chinese')),
    #  ('en', gettext('English')),
)

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440 * 4
FILE_UPLOAD_PERMISSIONS = None
FILE_UPLOAD_TEMP_DIR = None

# EasyThumbnail Settings
THUMBNAIL_ALIASES_ICON = {
    'xlarge': {
        'size': (150, 150),
        'quality': 85,
        'crop': False,
        'upscale': True,
        'format': 'jpg',
    },
    'large': {
        'size': (92, 92),
        'quality': 85,
        'crop': False,
        'upscale': True,
    },
    'middle': {
        'size': (72, 72),
        'quality': 85,
        'crop': False,
        'upscale': True,
    },
    'small': {
        'size': (48, 48),
        'quality': 85,
        'crop': False,
        'upscale': True,
    },
}
THUMBNAIL_ALIASES_COVER = {

    'large': {
        'size': (800, 480),
        'quality': 85,
        'crop': False,
        'upscale': True,
    },
    'middle': {
        'size': (480, 255),
        'quality': 85,
        'crop': False,
        'upscale': True,
    },
    'small': {
        'size': (450, 215),
        'quality': 85,
        'crop': False,
        'upscale': True,
    },
    'tiny': {
        'size': (190, 72),
        'quality': 85,
        'crop': False,
        'upscale': True,
    },
}
THUMBNAIL_ALIASES_SCREENSHOT = {
    'large': {
        'size': (480, 800),
        'quality': 85,
        'crop': False,
        'upscale': True,
    },
    'middle': {
        'size': (235, 390),
        'quality': 85,
        'crop': False,
        'upscale': True,
    },
    'small': {
        'size': (240, 400),
        'quality': 85,
        'crop': False,
        'upscale': True,
    },
}

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': 'smart'},
    },
    'account.Profile': dict(list(THUMBNAIL_ALIASES_ICON.items()) + \
                            list(dict(tiny=dict(size=(20, 20),
                                           quality=85,
                                           crop=False,
                                           upscale=True)).items())),
    'warehouse.PackageVersion.icon': THUMBNAIL_ALIASES_ICON,
    'warehouse.PackageVersion.cover': THUMBNAIL_ALIASES_COVER,
    'warehouse.PackageVersionScreenshot.image': THUMBNAIL_ALIASES_SCREENSHOT,
    'warehouse.Author.icon': THUMBNAIL_ALIASES_ICON,
    'warehouse.Author.cover': THUMBNAIL_ALIASES_COVER,
    'taxonomy.Category.icon': THUMBNAIL_ALIASES_ICON,
    'taxonomy.Topic.icon': THUMBNAIL_ALIASES_ICON,
    'taxonomy.Topic.cover': THUMBNAIL_ALIASES_COVER,
    'promotion.Advertisement.cover': THUMBNAIL_ALIASES_COVER,
    'account.Profile.cover': THUMBNAIL_ALIASES_COVER,
    'account.Profile.mugshot': THUMBNAIL_ALIASES_ICON,
}

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'toolkit.processors.scale_percents_and_crop',
    'easy_thumbnails.processors.filters',
)

REST_FRAMEWORK = {
    'DATE_FORMAT': 'iso-8601',
    'DATETIME_FORMAT': '%s',
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 50,

    #'DEFAULT_MODEL_SERIALIZER_CLASS':
    #    'rest_framework.serializers.HyperlinkedModelSerializer',

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'toolkit.renderers.BrowsableAPIRenderer',
    ),

    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
}

REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60
}

#SLUGFIELD_SLUGIFY_FUNCTION = ''
TAGGING_AUTOCOMPLETE_JS_BASE_URL = '/media/js'
MANDRILL_API_KEY = "brack3t-is-awesome"
#EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
DEFAULT_FROM_EMAIL = 'killua.vx@gmail.com'

SWAGGER_SETTINGS = {
    "exclude_namespaces": [], # List URL namespaces to ignore
    "api_version": '0.1', # Specify your API's version
    "enabled_methods": [# Specify which methods to enable in Swagger UI
                        'get',
                        'post',
                        'put',
                        'patch',
                        'delete'
    ],
    "api_key": '', # An API key
    "is_authenticated": False, # Set to True to enforce user authentication,
    "is_superuser": False, # Set to True to enforce admin only access
}


def NOW():
    from django.utils import timezone

    return timezone.now()

AUTHENTICATION_BACKENDS = (
    'guardian.backends.ObjectPermissionBackend',
    'account.backends.UCenterModelBackend',
    'account.backends.GameCenterModelBackend',
    'account.backends.GameCenterProfileBackend',
)
ANONYMOUS_USER_ID = -1

AUTH_USER_MODEL = 'account.User'
AUTH_PROFILE_MODULE = 'account.Profile'

#LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
#LOGIN_REDIRECT_URL = ''
SIGNUP_URL = '/accounts/signup/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'

AAPT_CMD = join(PROJECT_PATH, 'warehouse/utils/android-tools-linux-x64/aapt')

COMMENTS_APP = 'comment'

#COMMENTS_POST_PUBLISHED = False
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:8983/solr/package',
    },
    'package': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:8983/solr/package',
    },
}


import os
# for solr script

os.environ['SEARCHER_SCRIPT_DIR'] = SEARCHER_SCRIPT_DIR =\
    join(dirname(PROJECT_PATH), 'dependents/searcher')
os.environ['SEARCHER_SERVICE_CONF'] = SEARCHER_SERVICE_CONF =\
    join(os.environ['SEARCHER_SCRIPT_DIR'], 'solr.conf')
os.environ['SOLR_HOME'] = SOLR_HOME =\
    join(os.environ['SEARCHER_SCRIPT_DIR'], 'solr')


REDIS_SERVER_CMD='/usr/local/bin/redis-server'

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0
SESSION_REDIS_PASSWORD = ''
SESSION_REDIS_PREFIX = 'session'

CACHE_DEFAULT_LOCATION_REDIS = "127.0.0.1:6379:1"
CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": CACHE_DEFAULT_LOCATION_REDIS,
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
            }
    }
}

MOGOENGINE_SERVER_CMD = '/opt/local/bin/mongod'

MOGOENGINE_CLIENT_CMD = '/opt/local/bin/mongo'

FORUM_URL = 'http://bbs.ccplay.com.cn/'

DATABASE_ROUTERS = [
    'webservice.dbroute_settings.DatawarehouseRouter',
    'webservice.dbroute_settings.CrawlerRouter',
]


DEFAULT_FILE_STORAGE = 'toolkit.storage.QiniuResourceFileStorage'

FONT_DIRECTORY = join(STATIC_ROOT, 'common/font')


# celery
CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

import os
CELERY_BROKER_HOST = os.getenv('CELERY_BROKER_HOST', 'localhost')
BROKER_URL='redis://{0}:6379/2'.format(CELERY_BROKER_HOST)
CELERY_RESULT_HOST = os.getenv('CELERY_RESULT_HOST', 'localhost')
CELERY_RESULT_BACKEND = 'redis://{0}:6379/3'.format(CELERY_RESULT_HOST)

CELERY_ENABLE_UTC = True

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_TASK_RESULT_EXPIRES = 3600

CELERY_ROUTES = ({
    'analysis.tasks.record_event': {
        'queue': 'record_event',
        'exchange': 'analysis',
        'routing_key': 'analysis.record_event',
    },
}, )

from kombu import Queue, Exchange
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = [
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('record_event', Exchange('analysis'), routing_key='analysis.record_event'),
]

try:
    import djcelery
    djcelery.setup_loader()
except:
    pass


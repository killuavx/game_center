# -*- coding: utf-8 -*-
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
    'activity.Activity.cover': THUMBNAIL_ALIASES_COVER,
}


THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'toolkit.processors.scale_percents_and_crop',
    'easy_thumbnails.processors.filters',
)

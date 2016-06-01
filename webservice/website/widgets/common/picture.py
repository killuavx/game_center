# -*- coding: utf-8 -*-


class BasePictureShowcaseWidget(object):

    template = 'pages/widgets/home/picture-showcase.haml'

    def get_context(self, value=None, options=dict(), context=None):
        return options

# -*- coding: utf-8 -*-
from django_widgets import Widget

class AccountTopbarWdiget(Widget):

    template = 'pages/widgets/common/account-topbar.haml'

    def get_context(self, value=None, options=dict(), context=None):
        user = context.get('user')
        options.update(
            user=user
        )
        return options

# -*- coding: utf-8 -*-
from django_widgets import Widget

class ClientAppLatestDownloadWidget(Widget):

    def get_context(self, value=None, options=dict(), context=None):
        from clientapp.models import ClientPackageVersion
        package_name = options.get('package_name')
        item = None
        if package_name:
            try:
                item = ClientPackageVersion.objects\
                        .filter(package_name=package_name)\
                        .published().latest_version()
            except ClientPackageVersion.DoesNotExist:
                pass

        options.update(dict(
            item=item,
        ))
        return options

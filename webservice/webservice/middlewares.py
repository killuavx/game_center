from django.utils.translation import get_language


class RequestFillLanguageCodeMiddleware(object):

    def process_request(self, request):
        request.LANGUAGE_CODE = get_language()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class RequestBindRemoteAddrMethodMiddleware(object):

    def process_request(self, request):
        request.get_client_ip = lambda: get_client_ip(request)

from django.utils.translation import get_language

class RequestFillLanguageCodeMiddleware(object):

    def process_request(self, request):
        request.LANGUAGE_CODE = get_language()

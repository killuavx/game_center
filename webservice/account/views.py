# Create your views here.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action, link, permission_classes, authentication_classes
from rest_framework import (generics, mixins, viewsets )

class AccountViewSet(viewsets.ModelViewSet):

    @action(['post'])
    def signup(self, request, *args, **kwargs):
        pass

    @action(['post'], permission_classes=() )
    def signin(self, request, *args, **kwargs):
        obtain_auth_token = ObtainAuthToken()
        return obtain_auth_token.post(request)

    @action(['post'], permission_classes=(IsAuthenticated,))
    def set_password(self, request, *args, **kwargs):
        pass

    @link()
    def signout(self, request, *args, **kwargs):
        pass

    @link()
    @permission_classes([IsAuthenticated])
    def myprofile(self, request, *args, **kwargs):
        pass


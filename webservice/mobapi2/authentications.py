# -*- coding: utf-8 -*-
import pytz
from django.utils.timezone import datetime, timedelta
from rest_framework import exceptions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from account.models import User as Player


class ExpiringTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        # This is required for the time comparison
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - timedelta(hours=24):
            raise AuthenticationFailed('Token has expired')

        return token.user, token


class PlayerTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
        elif auth[1] == 'null':
            return None

        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, key):
        user, token = super(PlayerTokenAuthentication, self) \
            .authenticate_credentials(key)
        if user:
            user.__class__ = Player
        return (user, token)


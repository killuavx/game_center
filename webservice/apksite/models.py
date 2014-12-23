from django.db import models

# Create your models here.
from rest_framework.authtoken.models import Token as BaseToken
from account.models import Profile as BaseProfile, User as BaseUser


class Profile(BaseProfile):

    def _set_icon(self, icon_url):
        self._icon_url = icon_url

    def _get_icon(self):
        if hasattr(self, '_icon_url'):
            return self._icon_url
        return None

    icon = property(_get_icon, _set_icon)

    comment_count = None

    bookmark_count = None

    giftbag_count = None

    def save(self, *args, **kwargs):
        pass

    def delete(self, using=None):
        pass

    class Meta:
        proxy = True


class Token(BaseToken):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        proxy = True


class User(BaseUser):

    def _set_token(self, token_key):
        self.auth_token = Token(key=token_key, user=self)

    def _get_token(self):
        return self.auth_token.key

    token = property(_get_token, _set_token)

    @property
    def profile(self):
        if hasattr(self, '_profile_kwargs'):
            return self._profile
        return None

    @profile.setter
    def profile(self, kwargs):
        """
        			"token": "0388908ddf6144b49a11ef7da2b0643c",
			"id": 66863,
			"username": "rangervx",
			"icon": null,
			"email": null,
			"phone": null,
			"sex": null,
			"birthday": null,
			"comment_count": 0,
			"bookmark_count": 0,
			"giftbag_count": 0,
			"level": 0,
			"coin": 0,
			"experience": 0,
			"mugshot": null,
			"profile_id": 132832,
			"signup_date": "2014-12-18 17:56:57.001+08"

        """
        self._profile_kwargs = kwargs
        self._profile = Profile(id=kwargs.get('profile_id'),
                                phone=kwargs.get('phone'),
                                sex=kwargs.get('sex'),
                                level=kwargs.get('level'),
                                coin=kwargs.get('coin'),
                                user=self,
                                )
        self.token = kwargs.get('token')
        self._profile.icon = kwargs.get('icon')

    def save(self, *args, **kwargs):
        pass

    def delete(self, using=None):
        pass

    class Meta:
        proxy = True
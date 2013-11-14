# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from account.utils import *
from account import settings as account_settings

from django.contrib.auth import authenticate

USERNAME_RE = r'^[\.\w_]+$'

attrs_dict = {'class': 'required'}

required_message_template = '%s should not be empty.'


class SignupForm(forms.Form):

    username = forms.RegexField(regex=USERNAME_RE,
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _('Username must '
                                                'contain only letters, numbers,'
                                                ' dots and underscores.'),
                                                'required': _(required_message_template%"Username")})

    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                          render_value=False),
                               label=_("Create password"),
                               error_messages={'required': _(required_message_template%"Password")})

    def _random_email(self):
        identification = sha_constructor(str(random.random()).encode('utf-8'))\
                             .hexdigest()[:10]
        return "%s@%s" %(identification, 'uc.ccplay.com.cn')

    def _random_phone(self):
        now = get_datetime_now()
        return now.strftime('%Y%m%d%H%M%S%f')

    def clean_username(self):
        try:
            filters = dict(username__iexact=self.cleaned_data['username'])
            user = get_user_model().objects.get(**filters)
        except get_user_model().DoesNotExist:
            pass
        else:
            raise forms.ValidationError(_('This username is already taken.'))
        if self.cleaned_data['username'].lower() in account_settings.ACCOUNT_FORBIDDEN_USERNAMES:
            raise forms.ValidationError(_('This username is not allowed.'))
        self.cleaned_data['username'] = self.cleaned_data['username'].lower()
        return self.cleaned_data['username']

    def clean(self):
        self.cleaned_data['email'] = self._random_email()
        self.cleaned_data['phone'] = self._random_phone()
        return self.cleaned_data

    def save(self):
        username, email, phone, password =(self.cleaned_data['username'],
                                           self.cleaned_data['email'],
                                           self.cleaned_data['phone'],
                                           self.cleaned_data['password'])
        UserModel = get_user_model()
        user = UserModel.objects.create_user(username=username,
                                             password=password,
                                             email=email,
                                             phone=phone)
        return user




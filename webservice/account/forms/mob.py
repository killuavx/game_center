# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from kombu import uuid
from account.utils import *
from account import settings as account_settings
from account.models import Profile

from django.contrib.auth import authenticate

USERNAME_RE = r'^[\.\w_]+$'

attrs_dict = {'class': 'required'}

required_message_template = '%s should not be empty.'


class SignupForm(forms.Form):

    username = forms.RegexField(regex=USERNAME_RE,
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={
                                                #'invalid': _('Username must '
                                                #'contain only letters, numbers,'
                                                #' dots and underscores.'),
                                                'invalid': '用户名只能由数字字母组合',
                                                #'required': _(required_message_template%"Username")
                                                'required': '用户名不能为空'
                                })

    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                          render_value=False),
                               label=_("Create password"),
                               error_messages={
                                   #'required': _(required_message_template%"Password")
                                   'required': '密码不能为空'
                               })

    email = forms.EmailField(required=False)

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
            # _('This username is already taken.')
            raise forms.ValidationError('用户名已经注册了')
        if self.cleaned_data['username'].lower() in account_settings.ACCOUNT_FORBIDDEN_USERNAMES:
            # _('This username is not allowed.')
            raise forms.ValidationError('用户名不合法')
        self.cleaned_data['username'] = self.cleaned_data['username'].lower()
        return self.cleaned_data['username']

    def clean(self):
        if not self.cleaned_data['email']:
            self.cleaned_data['email'] = generate_random_email()
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


class DeviceAnonymousSignupForm(forms.Form):

    imei = forms.CharField(max_length=100)

    def _imei_identifier(self, imei):
        return sha_constructor(str(imei) .encode('utf-8')).hexdigest()[:20]

    def _random_phone(self):
        now = get_datetime_now()
        return now.strftime('%Y%m%d%H%M%S%f')

    def clean(self):
        self.cleaned_data['email'] = generate_random_email()
        self.cleaned_data['phone'] = self._random_phone()
        self.cleaned_data['password'] = uuid()
        self.cleaned_data['username'] = ("guest_%s" % self._imei_identifier(self.cleaned_data['imei'])).lower()
        return self.cleaned_data

    def save(self):
        try:
            profile = Profile.objects.get(imei=self.cleaned_data['imei'].lower())
        except Profile.DoesNotExist:
            username, email, phone, password =(self.cleaned_data['username'],
                                               self.cleaned_data['email'],
                                               self.cleaned_data['phone'],
                                               self.cleaned_data['password'])
            UserModel = get_user_model()
            user = UserModel.objects.create_user(username=username,
                                                 password=password,
                                                 email=email,
                                                 phone=phone)
            profile = user.profile
            profile.imei = self.cleaned_data['imei']
            profile.save()
            user.is_active = False
            user.save()
            return user
        else:
            return profile.user

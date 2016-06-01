# -*- coding: utf-8 -*-
from copy import deepcopy
from django import forms
from django.utils.translation import ugettext_lazy as _
from kombu import uuid
from account.utils import *
from account import settings as account_settings
from account.models import Profile
from account.validators import AccountUsernameForbiddenValidator, phone_re
from django.db import transaction, IntegrityError
from django.core import validators


USERNAME_RE = r'^[\.\w_]+$'

attrs_dict = {'class': 'required'}

required_message_template = '%s should not be empty.'


password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                      render_value=False),
                           label=_("Create password"),
                           validators=[
                               validators.MaxLengthValidator(16),
                               validators.MinLengthValidator(6),
                           ],
                           error_messages={
                               'required': '密码不能为空',
                               'max_length': '密码不能超过%(limit_value)s位',
                               'min_length': '密码至少填写%(limit_value)s位',
                           })


class SignupForm(forms.Form):

    username = forms.RegexField(regex=USERNAME_RE,
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                validators=[
                                    AccountUsernameForbiddenValidator()
                                ],
                                error_messages={
                                                #'invalid': _('Username must '
                                                #'contain only letters, numbers,'
                                                #' dots and underscores.'),
                                                'invalid': '用户名只能由数字字母组合',
                                                #'required': _(required_message_template%"Username")
                                                'required': '用户名不能为空'
                                })

    password = deepcopy(password)

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
        if not self.cleaned_data.get('email'):
            self.cleaned_data['email'] = generate_random_email()

        self.cleaned_data['phone'] = self._random_phone()
        return self.cleaned_data

    def save(self):
        username, email, phone, password =(self.cleaned_data['username'],
                                           self.cleaned_data.get('email'),
                                           self.cleaned_data['phone'],
                                           self.cleaned_data['password'])
        UserModel = get_user_model()
        user = UserModel.objects.create_user(username=username,
                                             password=password,
                                             email=email,
                                             phone=phone)
        return user


class BaseSignupForm(forms.Form):

    password = deepcopy(password)

    def save(self):
        username, email, phone, password =(self.cleaned_data['username'],
                                           self.cleaned_data['email'],
                                           self.cleaned_data['phone'],
                                           self.cleaned_data['password'])
        UserModel = get_user_model()
        try:
            sid = transaction.savepoint()
            user = UserModel.objects.create_user(username=username,
                                                 password=password,
                                                 email=email,
                                                 phone=phone)
            transaction.savepoint_commit(sid)
        except IntegrityError:
            transaction.rollback(sid)
            return None
        return user


def generate_random_phone():
    return get_datetime_now().strftime('%Y%m%d%H%M%S%f')


def generate_random_username():
    return uuid().replace("-", "")[0:10]


def validate_profile_unique_for(field, value, label):
    queryset = Profile.objects.all()
    if queryset.filter(**{field: value}).exists():
        raise validators.ValidationError('%s已被使用' %label, code='unique')


def validate_email_unique(val):
    validate_profile_unique_for(field='email', value=val, label='电子邮箱')


def validate_phone_unique(val):
    validate_profile_unique_for(field='phone', value=val, label='手机号码')


class EmailSignupForm(BaseSignupForm):

    username = forms.EmailField(error_messages={
        'invalid': '请填写有效电子邮箱',
        'required': '电子邮箱不能为空',
        },
                                label='Email',
                                validators=[validate_email_unique],
                                )

    def clean(self):
        self.cleaned_data['email'] = self.cleaned_data.get('username')
        self.cleaned_data['username'] = generate_random_username()
        self.cleaned_data['phone'] = generate_random_phone()
        return self.cleaned_data


from toolkit.CCPSDK.helpers import PhoneAuth


class PhoneSignupForm(BaseSignupForm):

    username = forms.RegexField(regex=phone_re,
                                label='Phone',
                                error_messages={
                                    'invalid': '请填写有效手机电话',
                                    'required': '手机电话不能为空',
                                    },
                                validators=[validate_phone_unique],
                             )

    code = forms.CharField(required=True,
                           label='验证码',
                           error_messages={
                               'invalid': '请填写有效验证码',
                               'required': '验证码不能为空',
                               },
                           )

    def clean(self):
        self.cleaned_data['phone'] = self.cleaned_data.get('username')
        phone_auth = PhoneAuth(phone=self.cleaned_data['phone'])
        if self.cleaned_data['phone'] and\
                not phone_auth.check_code(self.cleaned_data.get('code')):
            raise forms.ValidationError('验证码无效', code='invalid')

        self.cleaned_data['username'] = generate_random_username()
        self.cleaned_data['email'] = generate_random_email()
        return self.cleaned_data


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

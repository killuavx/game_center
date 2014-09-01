# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from mezzanine.accounts.forms import username_label
from mezzanine.utils.models import get_user_model
from account import settings as account_settings
from mezzanine.conf import settings
from mezzanine.accounts import get_profile_model, get_profile_user_fieldname
from account import authenticate
from django.utils.translation import ugettext as _
from django.utils.timezone import now
from toolkit.helpers import captcha as build_captcha


class CaptchaVerifyForm(forms.Form):
    captcha_verify = forms.CharField(max_length=8,
                                     required=False)

    captcha_key = 'captcha_verify'

    def __init__(self, request, check_captcha=True, **kwargs):
        self.request = request
        self.check_captcha = check_captcha
        super(CaptchaVerifyForm, self).__init__(**kwargs)

    def clean_captcha_verify(self):
        chk_captcha_verify = str(self.request.session.get(self.captcha_key, '')).lower()
        _captcha_verify = str(self.cleaned_data.get('captcha_verify', '')).lower()
        if self.check_captcha and chk_captcha_verify != _captcha_verify:
            raise forms.ValidationError('验证码无效')
        return _captcha_verify

    def build_captcha(self):
        img, self.request.session[self.captcha_key] = build_captcha()
        return img


class LoginForm(CaptchaVerifyForm):
    username = forms.CharField(label=username_label, error_messages={'required':'请输入账号'})
    password = forms.CharField(label=_("Password"),
                               error_messages={'required': '请输入密码'},
                               widget=forms.PasswordInput(render_value=False))

    app = forms.CharField(max_length=5, required=False)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        app = self.cleaned_data.get('app')
        app = app if app else None
        self._user = authenticate(username=username, password=password, app=app)
        if self._user is None:
            raise forms.ValidationError('无效用户名/邮箱或密码错误')
        elif not self._user.is_active:
            raise forms.ValidationError('你的账号未激活')
        return self.cleaned_data

    def save(self):
        return getattr(self, '_user', None)


User = get_user_model()
Profile = get_profile_model()


class SignupForm(CaptchaVerifyForm):

    username = forms.CharField(label='用户名')

    email = forms.EmailField(label='电子邮箱',
                             error_messages={'required': '请填写电子邮箱',
                                             'invalid': '请填写有效的电子邮箱',
                                             }
                             )

    password1 = forms.CharField(label='密码',
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label='确认密码',
                                widget=forms.PasswordInput(render_value=False))

    agree = forms.BooleanField(error_messages={'required': '请确认已阅读使用协议'})

    def clean(self):
        self.cleaned_data['phone'] = self._make_phone()
        return self.cleaned_data

    def clean_username(self):
        try:
            filters = dict(username__iexact=self.cleaned_data['username'])
            user = get_user_model().objects.get(**filters)
        except get_user_model().DoesNotExist:
            pass
        else:
            raise forms.ValidationError('用户名已经被注册')
        if self.cleaned_data['username'].lower() in account_settings.ACCOUNT_FORBIDDEN_USERNAMES:
            raise forms.ValidationError('用户名被禁止使用')
        self.cleaned_data['username'] = self.cleaned_data['username'].lower()
        return self.cleaned_data['username']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            Profile.objects.get(email__iexact=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('电子邮箱已经被注册')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1:
            errors = []
            if password1 != password2:
                errors.append('确认密码不正确')
            if len(password1) < settings.ACCOUNTS_MIN_PASSWORD_LENGTH:
                errors.append('密码至少%s个字符' %
                              settings.ACCOUNTS_MIN_PASSWORD_LENGTH)
            if errors:
                self._errors["password1"] = self.error_class(errors)
        return password2

    def _make_phone(self):
        return now().strftime('%Y%m%d%H%M%S%f')

    def save(self):
        username, email, phone, password =(self.cleaned_data['username'],
                                           self.cleaned_data['email'],
                                           self.cleaned_data['phone'],
                                           self.cleaned_data['password2'])
        user = User.objects.create_user(username=username,
                                        password=password,
                                        email=email,
                                        phone=phone)
        return user


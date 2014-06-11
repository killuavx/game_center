# -*- coding: utf-8 -*-
from django import forms
from mezzanine.accounts.forms import LoginForm, username_label
from account import authenticate
from django.utils.translation import ugettext as _


class LoginCaptchaForm(LoginForm):

    username = forms.CharField(label=username_label, error_messages={'required':'请输入账号'})
    password = forms.CharField(label=_("Password"),
                               error_messages={'required': '请输入密码'},
                               widget=forms.PasswordInput(render_value=False))

    app = forms.CharField(max_length=5, required=False)

    captcha_verify = forms.CharField(max_length=8,
                                     required=False)

    captcha_key = 'captcha_verify'


    def __init__(self, request, check_captcha=True, **kwargs):
        self.request = request
        self.check_captcha = check_captcha
        super(LoginCaptchaForm, self).__init__(**kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        app = self.cleaned_data.get('app')
        app = app if app else None
        self._user = authenticate(username=username, password=password, app=app)
        if self._user is None:
            raise forms.ValidationError('无效用户名/邮箱或码错误')
        elif not self._user.is_active:
            raise forms.ValidationError('你的账号未激活')
        return self.cleaned_data

    def clean_captcha_verify(self):
        chk_captcha_verify = str(self.request.session.get(self.captcha_key, '')).lower()
        _captcha_verify = str(self.cleaned_data.get('captcha_verify', '')).lower()
        if self.check_captcha and chk_captcha_verify != _captcha_verify:
            raise forms.ValidationError('验证码无效')
        return _captcha_verify

    def save(self):
        return getattr(self, '_user', None)


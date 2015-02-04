# -*- coding: utf-8 -*-
from datetime import datetime, time, timezone
from django import forms
from django.utils.encoding import force_text
from mezzanine.accounts.forms import username_label
from account.validators import AccountUsernameForbiddenValidator
from mezzanine.conf import settings
from django.utils.translation import ugettext as _
from toolkit.helpers import captcha as build_captcha
from iossite.utils import authenticate
from iossite.apis import ApiFactory, ApiResponseException
from iossite.backends import RemoteApiUserBackend


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
        data = dict(username=username, password=password, app=app)
        self._user = authenticate(**data)
        if self._user is None:
            raise forms.ValidationError('无效用户名/邮箱或密码错误')
        elif not self._user.is_active:
            raise forms.ValidationError('你的账号未激活')
        return self.cleaned_data

    def save(self):
        return getattr(self, '_user', None)


class SignupForm(CaptchaVerifyForm):

    username = forms.CharField(label='用户名',
                               validators=[
                                   #AccountUsernameForbiddenValidator()
                               ])

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
        if not self.cleaned_data.get('agree'):
            raise forms.ValidationError('请确认阅读使用协议')
        return self.cleaned_data

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

    def save(self):
        username, email, password =(self.cleaned_data['username'],
                                    self.cleaned_data['email'],
                                    self.cleaned_data['password2'])
        api = ApiFactory.factory('user.register')
        response = api.request(username=username, email=email, password=password)
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            raise forms.ValidationError(e.msg)
        return self.authenticate(result)

    def authenticate(self, result):
        backend = RemoteApiUserBackend()
        user = backend.wrapup_user(result)
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        return user



from django.contrib.comments import CommentForm
from comment.helpers import comment_forbidden_words
from comment.forms import ForbiddenWordValidator

COMMENT_MAX_LENGTH = 300


class CommentWithStarForm(CommentForm):

    email = forms.EmailField(required=False)

    name = forms.CharField(required=False)

    star = forms.IntegerField(label="评星",
                              widget=forms.HiddenInput(attrs={'id': 'rating_output', 'value': 3}))

    comment = forms.CharField(label=_('Comment'), widget=forms.Textarea,
                              min_length=3,
                              max_length=COMMENT_MAX_LENGTH,
                              validators=[
                                  #ForbiddenWordValidator(words=comment_forbidden_words, message='您的评论含有敏感词汇')
                              ])

    def __init__(self, request, **kwargs):
        self.request = request
        super(CommentWithStarForm, self).__init__(**kwargs)

    def clean_star(self):
        from mezzanine.conf import settings
        if self.cleaned_data['star'] not in settings.RATINGS_RANGE + [0]:
            raise forms.ValidationError('评星错误', code=1)
        return self.cleaned_data['star']

    def get_comment_model(self):
        return dict

    def save(self):
        ip_address = self.request.get_client_ip()
        token_key = self.request.user.token
        api = ApiFactory.factory('user.postComment')
        response = api.request(
            authorization_token=token_key,
            content_type=self.CONTENT_TYPE_ID,
            object_pk=self.cleaned_data['object_pk'],
            comment=self.cleaned_data['comment'],
            star=self.cleaned_data['star'],
            ip_address=ip_address,
        )
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            raise forms.ValidationError(e.msg)

        return result

    CONTENT_TYPE = 'warehouse.packageversion'

    CONTENT_TYPE_ID = 17

    def generate_security_data(self):
        """Generate a dict of security data for "initial" data."""
        timestamp = int(datetime.now().timestamp())
        security_dict =   {
            'content_type'  : self.CONTENT_TYPE,
            'object_pk'     : str(self.target_object.get('id', '')),
            'timestamp'     : str(timestamp),
            'security_hash' : self.initial_security_hash(timestamp),
            }
        return security_dict

    def initial_security_hash(self, timestamp):
        """
        Generate the initial security hash from self.content_object
        and a (unix) timestamp.
        """

        initial_security_dict = {
            'content_type' : self.CONTENT_TYPE,
            'object_pk' : str(self.target_object.get('id', '')),
            'timestamp' : str(timestamp),
            }
        return self.generate_security_hash(**initial_security_dict)

    def get_comment_create_data(self):
        return dict(
            content_type = str(self.CONTENT_TYPE_ID),
            object_pk    = force_text(self.target_object.get('id', '')),
            comment      = self.cleaned_data["comment"],
        )

    def get_comment_object(self):
        return self.get_comment_create_data()

    def clean_comment(self):
        return self.cleaned_data["comment"]

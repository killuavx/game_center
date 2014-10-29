# -*- coding: utf-8 -*-
import re
from django import forms
from toolkit.helpers import LazyIter
from comment.models import Feedback, FeedbackType
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core import validators
from comment.helpers import get_forbidden_words_from


class ForbiddenWordValidator(object):

    code = 'forbidden_words'

    message = "禁止词语: %(words)s"

    words = None

    def __init__(self, words, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.code = code
        self.words = words

    def __call__(self, value):
        words = self.words() if callable(self.words) else self.words
        forbidden_words = get_forbidden_words_from(words, value)
        if len(forbidden_words):
            raise ValidationError(self.message % {'words': ", ".join(forbidden_words)},
                                  code=self.code)


"""
def _feedback_kinds_setup():
    return FeedbackType.objects.all().values_list('slug', flat=True)


class PhoneValidator(validators.RegexValidator):
    regex = re.compile(r'^\+?\d+([\d-]+)$')

class FeedbackForm(forms.ModelForm):

    def __init__(self, user, request=None, *args, **kwargs):
        self.user = user
        self.request = request
        super(FeedbackForm, self).__init__(*args, **kwargs)

    kind = forms.RadioSelect(choices=LazyIter(_feedback_kinds_setup))

    contact_type = forms.RadioSelect(choices=('email', 'im_qq', 'phone'))

    contact_content = forms.CharField(required=False)

    comment = forms.Textarea()

    CONTACT_VALIDATORS = {
        'email': validators.EmailValidator,
        'phone': PhoneValidator,
        'im_qq': validators.validate_integer,
    }

    def clean(self):
        cleaned_data = super(FeedbackForm, self).clean()
        try:
            ct = ContentType.objects.get_for_model(cleaned_data['content_type'])
            ct_obj = ct.get_object_for_this_type(pk=cleaned_data['object_pk'])
        except ObjectDoesNotExist as e:
            raise forms.ValidationError('错误反馈内容')

        try:
            contact_type = self.cleaned_data['contact_type']
            self.CONTACT_VALIDATORS[contact_type](self.cleaned_data['contact_content'])
        except ValidationError as e:
            name = 'contact_content'
            self._errors[name] = self.error_class(e.messages)
            if name in self.cleaned_data:
                del self.cleaned_data[name]

        return self.cleaned_data

    def save(self, commit=True):
        if self.instance and not self.instance.user:
            self.instance.user = self.user

        if self.request and getattr(self.request, 'get_client_ip', None):
            self.instance.ip_address = self.request.get_client_ip()

        setattr(self.instance,
                "contact_%s" % self.cleaned_data['contact_type'],
                self.contact_content)

        return super(FeedbackForm, self).save(commit=commit)

    class Meta:
        model = Feedback
        fields = ('content_type_id', 'object_pk', 'kind', 'comment')
"""

# -*- encoding=utf-8 -*-
from django import forms
from tagging.fields import TagField
from tagging_autocomplete.widgets import TagAutocomplete

class TagFormMixin(forms.Form):
    tags = TagField(widget=TagAutocomplete())


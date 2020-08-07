from django import forms
from django.forms import ModelForm
from .models import Script


class ScriptEntryForm(ModelForm):
    class Meta:
        model = Script
        fields = ['name', 'text']



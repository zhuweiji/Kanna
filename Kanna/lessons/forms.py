from django import forms
from django.forms import ModelForm
from .models import Script, ScriptKeywords

class ScriptEntryForm(ModelForm):
    class Meta:
        model = Script
        fields = ['name', 'text']


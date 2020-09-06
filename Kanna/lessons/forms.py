from django import forms
from django.forms import ModelForm
from .models import *


class AnalysisCreateForm(forms.ModelForm):
    class Meta:
        model = AnalysisObj
        # exclude = ['user', 'date', 'score']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AnalysisCreateForm, self).__init__(*args, **kwargs)

    # def save(self, commit=True):
    #     inst = super(AnalysisCreateForm, self).save(commit=False)
    #     inst.author = self.user
    #     if commit:
    #         inst.save()
    #         self.save_m2m()
    #         print('complete')
    #     return inst


class ScriptCreateForm(forms.ModelForm):
    class Meta:
        model = Script
        fields = ['topic', 'text']

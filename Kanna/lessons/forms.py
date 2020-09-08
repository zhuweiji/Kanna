from django import forms
from django.forms import ModelForm
from .models import *


class AnalysisCreateForm(forms.ModelForm):
    class Meta:
        model = AnalysisObj
        exclude = ['user','date','score','highlights','highlights_missed','filler_words']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AnalysisCreateForm, self).__init__(*args, **kwargs)
    #     print(self.fields)
    #     print(self.request.user)
        # self.fields['user'] = self.request.user
        # print('\n\n\n\n\n', self.request)




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

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, get_user_model
from .models import *

User = get_user_model()


class AnalysisCreateForm(forms.ModelForm):
    class Meta:
        model = AnalysisObj
        exclude = ['user', 'date', 'score', 'highlights', 'highlights_missed', 'filler_words']

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


class TutorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_tutor = True
        if commit:
            user.save()
        return user


class TopicCreateForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = "__all__"


class ScriptCreateForm(forms.ModelForm):
    class Meta:
        model = Script
        fields = ['topic', 'text']


class SimpleAudioForm(forms.ModelForm):
    class Meta:
        model = SimpleAudioFile
        fields = ("topic", "filename")

    def clean(self):
        """ checks that uploaded audio is of acceptable type """
        accepted_extensions = ['m4a', 'wav', 'mp3']

        cleaned_data = super().clean()
        file = cleaned_data.get('filename')
        file_extension = str(file).split('.')[1]

        if file_extension.lower() not in accepted_extensions:
            raise forms.ValidationError(f"Audio must be either {(','.join(accepted_extensions))}")

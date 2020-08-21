from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, FormView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import *
from .forms import *

from .forms import *

@login_required
def index(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    context = {
        'user': user
    }
    return render(request, 'index.html', context=context)


class ScriptListView(LoginRequiredMixin, generic.ListView):
    model = Script
    template_name = 'script_list.html'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user if self.request.user.is_authenticated else None
        context['user'] = user
        return context


class ScriptDetailView(LoginRequiredMixin, generic.DetailView):
    model = Script
    template_name = 'script_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user if self.request.user.is_authenticated else None
        context['user'] = user
        return context


class TranscriptListView(LoginRequiredMixin, generic.ListView):
    model = Transcript
    template_name = 'transcript_list.html'


class TranscriptDetailView(LoginRequiredMixin, generic.DetailView):
    model = Transcript
    template_name = 'transcript_detail.html'

    def add_transcript_to_session(self):
        pass


class CreateScriptView(CreateView):
    template_name = 'script_create.html'
    form_class = ScriptCreateForm


class AnalysisObjView(LoginRequiredMixin, generic.DetailView):
    model = AnalysisObj
    template_name = 'analysis_detail.html'
    context_object_name = 'instance'


@login_required
def record(request):
    context = {

    }
    return render(request, 'record.html', context=context)


class ScriptEditorView(View):
    def get(self, request, pk, *args, **kwargs):
        script = Script.objects.get(pk=pk)
        context = {
            'script': script,
        }
        if request.is_ajax():
            script_functions = ['highlight', 'reset', 'save']
            ajax_function = request.GET.get('method')
            if ajax_function == 'reset':
                script.flags = script.default_script_flags()
                script.save()
                return render(request, 'editor.html', context=context)

            elif ajax_function == 'save':
                text = request.GET.get('text')
                self.mark_flags(text, script)
                return redirect('index')

        return render(request, 'editor.html', context=context)

    @staticmethod
    def mark_flags(htmltext, script):
        markers = ['<span', 'class="highlighted">', '</span>']
        text = htmltext.split()
        print(text)
        print(text[2])
        script_flags = script.flags

        word_counter = 0
        is_highlighted = False
        for word in text:
            if word.find(markers[1]) != -1:
                is_highlighted = True

            if is_highlighted:
                script_flags[word_counter] = 1

            else:
                script_flags[word_counter] = 0

            if word.find(markers[2]) != -1:
                is_highlighted = False

            print(word, script_flags[word_counter], word_counter)

            word_counter += 1 if word not in markers else 0

        if len(script.text.split()) != len(script_flags):
            print('\n\n\n\n--------------------')
            print('flag and text mismatch')
            print(len(script.text.split()))
            print(len(script_flags))
        script.flags = script_flags
        script.save()


class AnalysisCreateView(LoginRequiredMixin, CreateView):
    template_name = 'analysis.html'
    form_class = AnalysisCreateForm
    success_url = 'index'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


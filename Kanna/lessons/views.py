from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import *

from .forms import *

# Create your views here.


# class LoginRequiredView(LoginRequiredMixin, View):
#     login_url = 'accounts/login/'
#     redirect_field_name = 'lessons'

@login_required
def index(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    context = {
        'user': user
    }
    return render(request, 'index.html', context=context)

#
# def select_script(request):
#     context = {
#         'script_list': Script.objects.all(),
#
#     }
#     print(context['script_list'])
#     return render(request,'script_list.html', context=context)


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


class SelectTranscriptView(generic.detail.SingleObjectMixin, View):
    model = Transcript

    def post(self, request, *args, **kwargs):
        myobj = self.get_object()
        request.session['selected_transcript'] = myobj.id
        return redirect(...)


class CreateScriptView(CreateView):
    template_name = 'script_create.html'
    form_class = ScriptCreateForm


# class PreAnalysisView(CreateView):
#     template_name = 'preanalysis.html'
#     form_class = AnalysisCreateForm
#
#     def form_valid(self, form):
#         forminstace = form.save(commit=False)
#         forminstace.user = CustomUser.objects.get(self.request.user)
#         forminstace.save()
# def create_analysis_obj(request, pk):
#     analysis_instance = get_object_or_404(AnalysisObj, pk=pk)
#     if request.method == 'POST':
#         form = AnalysisCreateForm(request.POST, user=request.user)
#
#         if form.is_valid():
#             analysis_instance

# def analysis(request):
#     context = {
#     }
#     return render(request, 'index.html', context=context)


class AnalysisObjView(LoginRequiredMixin, generic.DetailView):
    model = AnalysisObj
    template_name = 'analysis_detail.html'
    context_object_name = 'instance'


@login_required
def analysis(request):
    context = {

    }
    return render(request, 'analysis.html', context=context)


@login_required
def record(request):
    context = {

    }
    return render(request, 'record.html', context=context)


def markkeywords(request, pk):
    context = {
        'transcript': Transcript.objects.get(pk=pk)
    }
    if request.method == "GET":
        print('its a get request')
        text = request.GET.get('selected_text')
        print(text)
    if request.method == 'POST':
        print('its a post request')

    return render(request, 'editor.html', context=context)


class TranscriptEditorView(View):
    model = Transcript
    template_name = 'editor.html'
    context_object_name = 'transcript'

    def get(self, request, pk, *args, **kwargs):
        context = {
            'transcript': Transcript.objects.get(pk=pk)
        }
        text = request.GET.get('selected_text')
        print('text:', text)
        print(request.GET.get('test_text'))

        return render(request, 'editor.html', context=context)


class TestAjax(View):
    def get(self, request):
        print(request)
        return render(request, 'test.html')


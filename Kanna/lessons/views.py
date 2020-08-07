from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import *

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


# def analysis(request):
#     context = {
#     }
#     return render(request, 'index.html', context=context)


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


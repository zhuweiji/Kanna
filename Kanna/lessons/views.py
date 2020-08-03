from django.shortcuts import render
from django.views import generic
from .models import *

# Create your views here.


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


class ScriptListView(generic.ListView):
    model = Script
    template_name = 'script_list.html'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user if self.request.user.is_authenticated else None
        context['user'] = user
        return context

    def update_selected_script(self, script):
        self.request.session['script'] = script
        print(self.request.session['script'])


class ScriptDetailView(generic.DetailView):
    model = Script
    template_name = 'script_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user if self.request.user.is_authenticated else None
        context['user'] = user
        return context


class TranscriptListView(generic.ListView):
    model = Transcript
    template_name = 'transcript_list.html'


class TranscriptDetailView(generic.DetailView):
    model = Transcript
    template_name = 'transcript_detail.html'

    def add_transcript_to_session(self):
        self.request.session['transcript'] = self.request.transcript
        print(self.request.session)
# def analysis(request):
#     context = {
#     }
#     return render(request, 'index.html', context=context)


def analysis(request):
    context = {

    }
    return render(request, 'analysis.html', context=context)


def record(request):
    context = {

    }
    return render(request, 'record.html', context=context)


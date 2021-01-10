from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, FormView, DetailView
from django.shortcuts import render
from django import template
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from .models import *
from .forms import *
from .services import listify, google_transcribe
from difflib import SequenceMatcher
import os
import io

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


class ScriptDetailView(LoginRequiredMixin, DetailView):
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


class TranscriptDetailView(LoginRequiredMixin, DetailView):
    model = Transcript
    template_name = 'transcript_detail.html'

    def add_transcript_to_session(self):
        pass


class CreateScriptView(LoginRequiredMixin, CreateView):
    template_name = 'script_create.html'
    form_class = ScriptCreateForm


class RecordView(LoginRequiredMixin, View):
    def get(self, request):
        form = SimpleAudioForm()

        context = {
            'form': form,
        }
        return render(request, 'record.html', context=context)

    def post(self, request):
        """ save recorded audio blob or uploaded audio by user """
        if request.method == "POST":
            form = SimpleAudioForm(request.POST, request.FILES)

            if form.is_valid():
                newobj = form.save()
                audio_filepath = os.path.join(settings.MEDIA_ROOT, newobj.filename.name)
                # filename is relative path from media dir in lessons
                # newobj.filename.name is true filename

                print(newobj.filename)
                try:
                    text = google_transcribe(audio_filepath)
                    newobj.creator = request.user
                    newobj.original_transcription = text
                    newobj.text = text

                except Exception as e:
                    raise e

                newobj.save()

                return redirect(newobj)
            else:
                form = SimpleAudioForm()
            context = {
                'form': form,
            }
            return render(request, 'record.html', context=context)


class AudioUploadSuccessView(LoginRequiredMixin, View):
    # model = SimpleAudioFile
    # template_name = 'simpleaudiofile_detail.html'

    def get(self, request, pk, *args, **kwags):
        audioobj = SimpleAudioFile.objects.get(pk=pk)
        all_script_objs = Script.objects.all()

        context = {
            'audioobj': audioobj,
            'scripts': all_script_objs,
        }

        similiarity = request.session.get('similarity', False)

        print([i for i in request.session.items()])

        if similiarity:
            del(request.session['similarity'])
            context['similarity'] = similiarity

        if request.is_ajax():
            ajax_function = request.GET.get('method')
            if ajax_function == 'transcribe':
                # audio relative filepath is saved as field named 'audio'
                audio_filepath = os.path.join(settings.MEDIA_ROOT, audioobj.filename.name)

                text = google_transcribe(audio_filepath)
                audioobj.original_transcription = text
                audioobj.text = text

                audioobj.save()

                return render(request, 'simpleaudiofile_detail.html', context=context)

            elif ajax_function == 'save':
                text = request.GET.get('text')
                print(text)
                audioobj.text = text
                audioobj.save()

                return render(request, 'simpleaudiofile_detail.html', context=context)

            elif ajax_function == 'analyse':
                print(audioobj.text)
                script_id = request.GET.get('script')

                script = Script.objects.get(pk=script_id)
                print(script.text)

                def similar(a, b):
                    """ placeholder similarity comparison"""
                    return SequenceMatcher(None, a, b).ratio()

                similarity = similar(audioobj.text, script.text)
                request.session['similarity'] = similarity

                # todo implement view to see changes

                return render(request, 'simpleaudiofile_detail.html', context=context)

        else:
            if similiarity:
                print(similiarity)
            else:
                print('similarity not present')
            return render(request, 'simpleaudiofile_detail.html', context=context)


class CompletedAnalysisView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            # 'similarity': request.session['similarity'],
        }
        return render(request, '(deprec)completed_analysis.html', context=context)


class SimpleAudioFileListView(LoginRequiredMixin, generic.ListView):
    model = SimpleAudioFile
    template_name = 'simpleaudiofilelistview.html'


class ScriptEditorView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        """ """
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

            # print(word, script_flags[word_counter], word_counter)
            word_counter += 1 if (word not in markers and word_counter < len(script_flags) - 1) else 0

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

    # success_url = reverse_lazy('index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AnalysisListView(LoginRequiredMixin, generic.ListView):
    model = AnalysisObj
    template_name = 'analysis_list.html'


class AnalysisObjView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        instance = AnalysisObj.objects.get(pk=pk)
        misses = instance.highlights_missed
        if not instance.highlights:
            return redirect('mark_keywords', pk=instance.script.pk)

        highlights = instance.highlights.split()
        missed_words = highlights
        misses = misses.strip('][').split(', ')
        print(misses)
        print(type(misses))

        if all(items == 0 for items in misses):  # redirects unhighlighted scripts to editor page
            return redirect('mark_keywords', pk=instance.script.pk)

        misses_ptr = 0
        no_misses = True
        for i, j in enumerate(highlights):
            if misses[misses_ptr] == '1':
                missed_words[i] = '<span style="background:#800000">' + missed_words[i] + '</span>'
                no_misses = False

            try:
                if misses[misses_ptr + 1] == '2':
                    missed_words[i] = missed_words[i] + "<br>"
                    misses_ptr += 1
            except IndexError:
                pass

            misses_ptr += 1
        context = {
            'instance': instance,
            'missed_words': ' '.join(missed_words),
            'no_misses': no_misses
        }

        if request.is_ajax():
            print(request)
            ajax_function = request.GET.get('method')
            print(ajax_function)
            if ajax_function == 'analyse':
                instance.full_analysis()
                instance.save()

        return render(request, 'analysis_detail.html', context=context)

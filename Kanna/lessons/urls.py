from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('record', views.RecordView.as_view(), name='record'),

    path('script', views.ScriptListView.as_view(), name='script_list'),
    path('script/<int:pk>', views.ScriptDetailView.as_view(), name='script_analysis'),
    path('script/create', views.CreateScriptView.as_view(), name='script_create'),

    path('mark/<int:pk>', views.ScriptEditorView.as_view(), name='mark_keywords'),


    path('uploadsuccess/<int:pk>', views.AudioUploadSuccessView.as_view(), name='upload_audio_success'),
    path('audiolist', views.SimpleAudioFileListView.as_view(), name='audio_list_view'),


    # unused
    #   -----------------------------------------------------------------------------
    path('transcript', views.TranscriptListView.as_view(), name='transcript_list'),
    path('transcript/<int:pk>', views.TranscriptDetailView.as_view(), name='transcript_detail'),
    #   ------------------------------------------------------------------------------
    path('start_new_analysis', views.AnalysisCreateView.as_view(), name='analyse'),
    path('analyse', views.AnalysisListView.as_view(), name='analyse_list'),
    path('analyse/<int:pk>', views.AnalysisObjView.as_view(), name='analyse_detail'),

]
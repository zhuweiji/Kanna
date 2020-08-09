from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('record', views.record, name='record'),

    path('script', views.ScriptListView.as_view(), name='script_list'),
    path('script/<int:pk>', views.ScriptDetailView.as_view(), name='script_analysis'),
    path('script/create', views.CreateScriptView.as_view(), name='script_create'),

    path('transcript', views.TranscriptListView.as_view(), name='transcript_list'),
    path('transcript/<int:pk>', views.TranscriptDetailView.as_view(), name='transcript_detail'),

    path('mark/<int:pk>', views.TranscriptEditorView.as_view(), name='mark_keywords'),

    path('analyse/<int:pk>', views.AnalysisObjView.as_view(), name='analyse_detail'),

    path('test', views.TestAjax.as_view(), name='test'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('record', views.record, name='record'),
    path('analysis', views.ScriptListView.as_view(), name='script_list'),
    path('analysis/<int:pk>', views.ScriptDetailView.as_view(), name='script_analysis'),
    path('transcript', views.TranscriptListView.as_view(), name='transcript_list'),
    path('transcript/<int:pk>', views.TranscriptDetailView.as_view(), name='transcript_detail'),
    path('test', views.SelectTranscriptView, name='star')
]
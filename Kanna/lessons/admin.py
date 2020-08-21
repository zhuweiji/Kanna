from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    # exclude = ('flags',)
    pass

@admin.register(AnalysisObj)
class AnalysisObjAdmin(admin.ModelAdmin):
    list_display = ['transcript','script','user','date','score','analyse']

admin.site.register(Transcript)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Topic)

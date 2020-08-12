from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    pass
    # exclude = ('flags',)

admin.site.register(Transcript)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(AnalysisObj)
admin.site.register(Topic)

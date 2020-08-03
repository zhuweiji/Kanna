from django.contrib import admin
from .models import Script, ScriptKeywords, Transcript

# Register your models here.

admin.site.register(ScriptKeywords)
admin.site.register(Script)
admin.site.register(Transcript)
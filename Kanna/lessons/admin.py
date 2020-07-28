from django.contrib import admin
from .models import Script, ScriptKeywords

# Register your models here.

admin.site.register(ScriptKeywords)
admin.site.register(Script)
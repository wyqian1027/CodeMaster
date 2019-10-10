from django.contrib import admin
from .models import Language, Library, Method
from tinymce.widgets import TinyMCE
from django.db import models

class MethodAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }   




admin.site.register(Language)
admin.site.register(Library)
admin.site.register(Method, MethodAdmin)
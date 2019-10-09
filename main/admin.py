from django.contrib import admin
from .models import Language, Library, Method
# from tinymce.widgets import TinyMCE
from django.db import models

admin.site.register(Language)
admin.site.register(Library)
admin.site.register(Method)
from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Language, Library, Method
# from tinymce.widgets import TinyMCE

class NewLangForm(ModelForm):

    class Meta:
        model = Language
        fields = ("language_name", )



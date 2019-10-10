from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Language, Library, Method
from tinymce.widgets import TinyMCE

class NewLangForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewLangForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
    class Meta:
        model = Language
        fields = ("language_name", )

class NewLibForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewLibForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
    class Meta:
        model = Library
        fields = ("library_name", "parent_language")
    
    parent_language = forms.ModelChoiceField(queryset=Language.objects.all(), required=True)

class NewMethodForm1(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewMethodForm1, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    class Meta:
        model = Method
        fields = ("parent_language", )
    
    parent_language = forms.ModelChoiceField(queryset=Language.objects.all(), required=True)

class NewMethodForm2(ModelForm):

    long_description = forms.CharField(required=False, widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    def __init__(self, *args, **kwargs):
        parent_lang_id = kwargs.pop('parent_lang_id')
        super(NewMethodForm2, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
        self.fields['parent_language'] = forms.ModelChoiceField(queryset=Language.objects.all(), initial=parent_lang_id, required=True)
        self.fields['parent_language'].widget.attrs.update({'class': 'form-control'})
        self.fields['parent_library'] = forms.ModelChoiceField(queryset=Library.objects.filter(parent_language__id=parent_lang_id), required=True)
        self.fields['parent_library'].widget.attrs.update({'class': 'form-control'})
        
    class Meta:
        model = Method
        fields = ("parent_language", "parent_library", "method_name", "use_example", "short_description",)
        


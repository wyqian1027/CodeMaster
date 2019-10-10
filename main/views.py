from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# from django.utils.timezone import now
from django.db.models import Q


from .models import Language, Library, Method
from .forms import NewLangForm, NewLibForm, NewMethodForm1, NewMethodForm2

def find_method(_language_name, _library_name, _method_name):
    return Method.objects.filter(Q(method_name=_method_name) & Q(parent_library__library_name=_library_name) & Q(parent_language__language_name=_language_name))

def find_library(_language_name, _library_name):
    return Library.objects.filter(Q(library_name=_library_name) & Q(parent_language__language_name=_language_name))

def find_language(_language_name):
    return Language.objects.filter(language_name=_language_name)

def find_all_methods_by_language(_language_name):
    return Method.objects.filter(parent_language__language_name=_language_name)

def find_all_methods_by_library(_language_name, _library_name):
    return Method.objects.filter(Q(parent_language__language_name=_language_name) & Q(parent_library__library_name=_library_name))


def index(request):
    return render(request=request,
                  template_name="main/index.html",
                  context={"languageCount" : Language.objects.all().count(),
                           "libraryCount"  : Library.objects.all().count(),
                           "methodCount"   : Method.objects.all().count(),
                           "methods"       : Method.objects.all(),  
                 })

def find_method_request(request, language_name, library_name, method_name):
    current_method = find_method(language_name, library_name, method_name)
    
    return render(request=request,
                  template_name="main/index.html",
                  context={"methods"        : current_method, 
                           "language_name"  : language_name,
                           "library_name"   : library_name,
                           "method_name"    : method_name,  
                           "longDescription": current_method.first().long_description,
                  })

def find_library_request(request, language_name, library_name):
    return render(request=request,
                  template_name="main/index.html",
                  context={"methods"        : find_all_methods_by_library(language_name, library_name), 
                           "language_name"  : language_name,
                           "library_name"   : library_name,
                  })

def find_language_request(request, language_name):
    
    return render(request=request,
                  template_name="main/index.html",
                  context={"methods"        : find_all_methods_by_language(language_name), 
                           "language_name"  : language_name,
                  })


def add_new_language_request(request):

    if request.method == "POST":
        form = NewLangForm(request.POST)
        if form.is_valid():
            new_lang = form.save(commit=False)
            new_lang_name = new_lang.language_name
            if find_language(new_lang_name).count() > 0:
                messages.warning(request, f"Language {new_lang_name} already exists!")
                return redirect(f"/all/{new_lang_name}")			
            new_lang.save()
            messages.success(request, f"Language {new_lang_name} created.") 
            return redirect(f"/all/{new_lang_name}")
        else:
            for msg in form.error_messages:
                messages.warning(request, f"{msg}:{form.error_messages[msg]}")
            return redirect("main:homepage")	    	

    form = NewLangForm()
    return render(request=request,
                  template_name="main/add_lang_form.html",
                  context={"form": form, "subtitle": "Add New Language"})

def add_new_library_request(request):

    if request.method == "POST":
        form = NewLibForm(request.POST)
        if form.is_valid():
            new_lib = form.save(commit=False)
            new_lib_name = new_lib.library_name
            parent_language = new_lib.parent_language.language_name
            if find_library(parent_language, new_lib_name).count() > 0:
                messages.warning(request, f"Library {new_lib_name} already exists!")
                return redirect(f"/all/{parent_language}/{new_lib_name}")			
            new_lib.save()
            messages.success(request, f"Library {new_lib_name} under {parent_language} created.") 
            return redirect(f"/all/{parent_language}/{new_lib_name}")
        else:
            for msg in form.error_messages:
                messages.warning(request, f"{msg}:{form.error_messages[msg]}")
            return redirect("main:homepage")	    	

    form = NewLibForm()
    return render(request=request,
                  template_name="main/add_lib_form.html",
                  context={"form": form, "subtitle": "Add New Library"})

def add_new_method_request(request):

    if request.method == "POST":
        form = NewMethodForm1(request.POST)
        if form.is_valid():
            new_method = form.save(commit=False)
            parent_language_id = new_method.parent_language.id
            return redirect(f"/add_meth/{parent_language_id}")
            
        else:
            for msg in form.error_messages:
                messages.warning(request, f"{msg}:{form.error_messages[msg]}")
            return redirect("main:homepage")	    	

    form = NewMethodForm1()
    return render(request=request,
                  template_name="main/add_method_form1.html",
                  context={"form": form, "subtitle": "Add New Method"})


def add_new_method_request_helper(request, language_id):
    
    if request.method == "POST":
        form = NewMethodForm2(request.POST, parent_lang_id=language_id)
        if form.is_valid():
            new_method = form.save(commit=False)
            method_name = new_method.method_name
            method_lib = new_method.parent_library.library_name
            method_lang = new_method.parent_language.language_name
            if find_method(method_lang, method_lib, method_name).count() > 0:
                messages.warning(request, f"Method {method_name} already exists!")
                return redirect(f"/all/{method_lang}/{method_lib}/{method_name}")
            new_method.long_description = form.cleaned_data.get('long_description')
            new_method.save()
            messages.success(request, f"Library {method_name} from Library {method_lib} created.") 
            return redirect(f"/all/{method_lang}/{method_lib}/{method_name}")
        else:
            for msg in form.error_messages:
                messages.warning(request, f"{msg}:{form.error_messages[msg]}")
            return redirect("main:homepage")	
    
    form = NewMethodForm2(parent_lang_id=language_id)
    return render(request=request,
                  template_name="main/add_method_form2.html",
                  context={"form": form, "subtitle": "Add New Method"})
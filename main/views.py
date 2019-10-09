from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# from django.utils.timezone import now
from django.db.models import Q


from .models import Language, Library, Method
from .forms import NewLangForm

def find_by_method(_language_name, _library_name, _method_name):
    return Method.objects.filter(Q(method_name=_method_name) & Q(parent_library__library_name=_library_name) & Q(parent_language__language_name=_language_name))

def find_by_library(_language_name, _library_name):
    return Method.objects.filter(Q(parent_library__library_name=_library_name) & Q(parent_language__language_name=_language_name))

def find_by_language(_language_name):
    return Method.objects.filter(Q(parent_language__language_name=_language_name))



def index(request):
	return render(request=request,
				  template_name="main/index.html",
				  context={"languageCount" : Language.objects.all().count(),
						   "libraryCount"  : Library.objects.all().count(),
						   "methodCount"   : Method.objects.all().count(),
                           "methods"       : Method.objects.all(),  
                           "subtitle"      : "Home",     
                 })

def find_method_request(request, language_name, library_name, method_name):
    return render(request=request,
                  template_name="main/index.html",
                  context={"methods"        : find_by_method(language_name, library_name, method_name), 
                           "language_name"  : language_name,
                           "library_name"   : library_name,
                           "method_name"    : method_name,     
                  })

def find_library_request(request, language_name, library_name):
    return render(request=request,
                  template_name="main/index.html",
                  context={"methods"        : find_by_library(language_name, library_name), 
                           "language_name"  : language_name,
                           "library_name"   : library_name,
                  })

def find_language_request(request, language_name):
    return render(request=request,
                  template_name="main/index.html",
                  context={"methods"        : find_by_language(language_name), 
                           "language_name"  : language_name,
                  })


def add_new_language_request(request):

	if request.method == "POST":
		form = NewLangForm(request.POST)
		if form.is_valid():
			new_lang = form.save(commit=False)
			new_lang_name = new_lang.language_name
			
			# checking cur category is duplicated
			if find_by_language(new_lang_name).count() > 0:
				messages.error(request, f"Language {new_lang_name} already exists!")
				return redirect(f"/all/{new_lang_name}")

			
			new_lang.save()
			messages.success(request, f"Language {new_lang_name} created.") 
			return redirect(f"/all/{new_lang_name}")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages[msg]}")
			return redirect("main:homepage")	    	

	form = NewLangForm()
	return render(request=request,
				  template_name="main/add_lang_form.html",
				   context={"form": form})

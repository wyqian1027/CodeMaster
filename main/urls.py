from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
	path('', views.index, name='homepage'),
    path('all/<language_name>/<library_name>/<method_name>', views.find_method_request, name='findMethodRequest'),
    path('all/<language_name>/<library_name>', views.find_library_request, name='findLibraryRequest'),
    path('all/<language_name>', views.find_language_request, name='findLanguageRequest'),
    path('add_lang', views.add_new_language_request, name='addLangRequest'),
]
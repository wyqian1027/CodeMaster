from django.urls import path, include
from . import views

app_name = "main"

urlpatterns = [
	path('', views.index, name='homepage'),
    path('all/<language_name>/<library_name>/<method_name>', views.find_method_request, name='findMethodRequest'),
    path('all/<language_name>/<library_name>', views.find_library_request, name='findLibraryRequest'),
    path('all/<language_name>', views.find_language_request, name='findLanguageRequest'),
    path('add_lang', views.add_new_language_request, name='addLangRequest'),
    path('add_lib', views.add_new_library_request, name='addLibRequest'),
    path('add_meth/<language_id>', views.add_new_method_request_helper, name='addMethRequestHelper'),
    path('add_meth', views.add_new_method_request, name='addMethRequest'),
    path('tinymce/', include('tinymce.urls')),

]
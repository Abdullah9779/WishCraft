from django.urls import path
from . import views

urlpatterns = [
    path('create-template/', view=views.create_template_api, name="create_template_api"),
    path('delete-template/', view=views.delete_template_api, name="delete_template_api"),
    path('contact/', view=views.contact_api, name="contact_api"),
]

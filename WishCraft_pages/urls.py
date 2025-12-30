from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.home_page, name="home_page"),
    path("view-template/<int:template_id>/", view=views.view_template_page, name="view_template_page"),
    path("create-template/<int:template_id>/", view=views.create_template_page, name="create_template_page"),
    path('s/<str:token>/', view=views.show_template, name="show_template"),
    path('template-url/<str:token>/', view=views.show_template_url, name="show_template_url"),
    path('my-templates/', view=views.my_templates_page, name="my_templates_page"),
    path('about/', view=views.about_page, name="about_page"),
    path('contact/', view=views.contact_page, name="contact_page"),
    path('privacy/', view=views.privacy_page, name="privacy_page"),
    path('install/', view=views.install_page, name="install_page"),
    path('blog/', view=views.blog_page, name="blog_page"),
]
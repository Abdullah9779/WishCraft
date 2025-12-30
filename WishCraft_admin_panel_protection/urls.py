from django.urls import path
from . import views

urlpatterns = [
    path('apwlr/<str:token>/', views.activate_user_sessions, name='activate_user_sessions'),
]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_login),
    path("register", views.user_register),
    path("logout", views.user_logout),
]

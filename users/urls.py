from django.contrib import admin
from django.urls import path, include
from . import views
from  django.urls import reverse


urlpatterns = [
    path('', views.login_page),
    path('registration/', views.registration),
    path('login/', views.login),
    path('profile/', views.profile_page)
]
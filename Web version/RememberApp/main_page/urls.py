from django.contrib import admin
from django.urls import path, include
from . import views
from  django.urls import reverse


urlpatterns = [
    path('', views.main_page),
    path('home/', views.main_page),
    path('lists/<str:search_try>/', views.searh_page),
    path('searching/', views.list_searching),
    #path('<int:search_try>/', views.redirect),,
    path('<str:search_try>/', views.searh_page),
]

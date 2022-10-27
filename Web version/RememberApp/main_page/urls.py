from django.contrib import admin
from django.urls import path, include
from . import views
from  django.urls import reverse


urlpatterns = [
    path('', views.main_page),
    path('home/', views.main_page),
    path('lists/<str:search_try>/', views.searh_page),
    path('creating_saving/', views.creating),
    path('searching/', views.list_searching),
    path('finding/<str:search_try>/', views.show_target_list),
    path('editing/<str:search_try>/', views.edit_target_list),
    path('update_saving/<str:search_try>/', views.update_saving),
    #path('<int:search_try>/', views.redirect),,
    path('<str:search_try>/', views.searh_page),
]

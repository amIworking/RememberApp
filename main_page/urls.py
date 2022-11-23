from django.contrib import admin
from django.urls import path, include
from . import views
from  django.urls import reverse


urlpatterns = [
    path('', views.main_page),
    path('home/', views.main_page),
    path('lists/<str:search_try>/', views.searh_page),
    path('creating_saving/', views.creating),
    path('searching/', views.dicts_searching),
    path('repeating/<str:search_try>/', views.repeat_dict),
    path('delete_confirming/<str:search_try>/', views.delete_confirming),
    path('deleting/<str:search_try>/', views.delete_dict),
    path('finding/<str:search_try>/', views.show_target_dict),
    path('editing/<str:search_try>/', views.edit_target_dict),
    path('update_saving/<str:search_try>/', views.update_saving),
    path('adding_dict/<str:search_try>/', views.adding_follow_dict),
    path('removing_dict/<str:search_try>/', views.remove_follow_dict),
    path('adding_points/<str:search_try>/', views.adding_points),
    #path('<int:search_try>/', views.redirect),
    path('speedtraining/', views.speed_training),
    path('<str:search_try>/', views.searh_page),
]

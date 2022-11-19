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
    path('repeating/<str:search_try>/', views.repeat_list),
    path('delete_confirming/<str:search_try>/', views.delete_confirming),
    path('deleting/<str:search_try>/', views.delete_list),
    path('finding/<str:search_try>/', views.show_target_list),
    path('editing/<str:search_try>/', views.edit_target_list),
    path('update_saving/<str:search_try>/', views.update_saving),
    path('adding_dict/<str:search_try>/', views.adding_follow_dict),
    path('removing_dict/<str:search_try>/', views.remove_follow_dict),
    #path('<int:search_try>/', views.redirect),
    path('speedtraining/', views.speed_training),
    path('<str:search_try>/', views.searh_page),
]

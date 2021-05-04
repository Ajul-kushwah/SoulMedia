from django.urls import path,include
from . import views

urlpatterns = [
    path('all_user', views.all_user, name='all_user'),
    path('all_suggest_user', views.all_suggest_user, name='all_suggest_user'),
    path('search_user', views.search_user, name='search_user'),

    # who profile view
    path('who_profile_view', views.who_profile_view, name='who_profile_view'),

    path('your_settings', views.your_settings, name='your_settings'),
    path('push_notifications', views.push_notifications, name='push_notifications'),
    path('other_details', views.other_details, name='other_details'),
    path('privacy_and_security', views.privacy_and_security, name='privacy_and_security'),

    path('states_load',views.states_load,name='states_load'),
    path('city_load',views.city_load,name='city_load'),




    path('userIndex', views.userIndex, name='userIndex'),
    path('userIndex2', views.userIndex2, name='userIndex2'),
    path('insta_profile', views.insta_profile, name='insta_profile'),

]

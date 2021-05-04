from django.urls import path,include
from .views import followers,followings
from .views import *

urlpatterns = [
    path('your_post', your_post, name='your_post'),
    path('followers', followers, name='followers'),
    path('followings', followings, name='followings'),
    path('create_post', create_post, name='create_post'),
    path('delete_post/<int:id>', delete_post, name='delete_post'),
    path('edit_post/<int:id>', edit_post, name='edit_post'),
    path('follow/<str:username>', follow, name='follow'),
    path('remove_follower/<str:username>', remove_follower, name='remove_follower'),

    # for all single post
    path('single_post/<int:id>', single_post, name='single_post'),

    # for all liked post
    path('liked_post', liked_post, name='liked_post'),
    # for like the post
    path('post_like', post_like, name='post_like'),
    # for all saved post
    path('all_saved_post', all_saved_post, name='all_saved_post'),

    # for save the post
    path('saved_post', saved_post, name='saved_post'),

    #other user post, followers and following
    path('<str:username>/post', other_user_post, name='other_user_post'),
    path('followings/<str:username>', other_user_followings, name='other_user_followings'),
    path('followers/<str:username>', other_user_followers, name='other_user_followers'),

]

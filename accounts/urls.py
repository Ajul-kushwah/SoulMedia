from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login_page', views.user_login, name='login_page'),
    path('demo_login', views.demo_login, name='demo_login'),
    path('register', views.user_register, name='register'),
    path('logout', views.user_logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('change_password', views.change_password, name='change_password'),

    path('_/<str:username>', views.other_user_profile, name='other_user_profile'),



    #username and email
    path('change_username',views.change_username,name='change_username'),
    path('change_email',views.change_email,name='change_email'),
    path('edit_account',views.edit_account,name='edit_account'),
    path('edit_other_detail',views.edit_other_detail,name='edit_other_detail'),
    path('change_profile',views.change_profile_img,name='change_profile'),

    #add bio
    path('add_bio',views.addBio,name='add_bio'),

    path('after_register', views.after_register, name='after_register'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('resendOTP', views.resend_otp),

    # reset password urls
    # path('password_reset/', auth_views.password_reset, name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_email.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_email.html'), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # alternative way to include authentication views
    path('', include('django.contrib.auth.urls')),


    #delete user account
    path('delete_account', views.delete_account, name='delete_account'),

    path('test', views.test, name='test'),

]


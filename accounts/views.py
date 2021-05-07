import datetime

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# models
from .models import *
from post.models import *

from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


@login_required
def index(request):
    post = Post.objects.all().order_by('-id')
    following_obj = Following.objects.get(user=request.user)
    followers_count, followings_count = following_obj.follower.count(), following_obj.followed.count()
    f =[request.user,'admin']
    for i in following_obj.followed.all():
        f.append(i.username)
    # print(f)
    suggestions_user = User.objects.exclude(username__in=f)[:2]
    # suggestions_userr = User.objects.exclude(username__in=f).order_by('?')
    context = {'post': post,
               'follower_count': followers_count,
               'followings_count': followings_count,
               'suggest_user': suggestions_user,
               'home':True
               }
    return render(request,'accounts/index.html',context)

def settings(request):
    return render(request,'settings/settings.html')

def demo_login(request):
    user = authenticate(username='demo',password='1234')
    if user is not None:
        login(request,user)
        return redirect('/')
    return redirect('login_page')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,
                            password = password)

        if user is not None:
            login(request, user)
            return redirect('index')
        elif not User.objects.filter(username=username).exists():
            messages.error(request, 'username & password Invalid')
            return redirect('login_page')
        elif not User.objects.get(username=username).is_active:
            usr = User.objects.get(username=username)

            # for otp with mail
            otp_with_mail(usr)

            messages.warning(request,'your account is not activate, we have send a otp at your registered email, please check mail and activate account.')
            return render(request,
                          'accounts/after_register.html',
                          {'username': usr.username, 'email': usr.email}
                          )

        else:
            messages.error(request,'username & password Invalid')
            return redirect('login_page')
    else:
        return render(request,'accounts/login.html')

import random
def user_register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        username = request.POST['user_name']
        password1 = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']

        if len(username) > 3:
            if ' ' not in username:
                if len(password1) >= 4:
                    if password1 == password2:
                        if User.objects.filter(username=username).exists():
                            messages.warning(request, 'username already exist ..')
                            print('username already exist ..')
                            return redirect('register')
                        elif User.objects.filter(email=email).exists():
                            messages.warning(request, 'email already exist..')
                            print('email already exist..')
                            return redirect('register')
                        else:
                            user = User.objects.create_user(username=username,
                                                            password=password1,
                                                            email=email,
                                                            first_name=firstname,
                                                            last_name=lastname,
                                                            is_active=False
                                                            )
                            user.save()
                            print('user created ')

                            usr = User.objects.get(username=username)

                            # for follow and userinfo
                            userinfo = UserInfo(user=usr,website=f'soulmedia.herokuapp.com/_/{usr.username}')
                            userinfo.save()
                            following = Following(user=usr)
                            following.save()

                            # for otp with mail
                            otp_with_mail(usr)

                            messages.success(request,'we have send otp to your email please check mail for verify account.')
                            return render(request,
                                          'accounts/after_register.html',
                                          {'username': usr.username, 'email': usr.email}
                                          )

                    else:
                        print('password not matching...')
                        messages.error(request, 'password not matching ..')
                        return redirect('register')
                else:
                    messages.warning(request,'password length should be of 4 or more.')
                    return redirect('register')
            else:
                messages.warning(request, 'username should not contains spaces.')
                return redirect('register')
        else:
            messages.warning(request,'username should have more than 3 characters.')
            return redirect('register')
    else:
        return render(request,'accounts/register.html')

def after_register(request):
    return render(request,'accounts/after_register.html')

def verify_otp(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        get_usr = request.POST.get('username')
        get_email = request.POST.get('email')

        usr = User.objects.get(username=get_usr)
        if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
            usr.is_active = True
            usr.save()
            messages.success(request, f'Account is verified For {usr.username} please login')
            return redirect('login_page')
        else:
            messages.warning(request, f'You Entered a Wrong OTP')
            return render(request,
                          'accounts/after_register.html',
                          {'username': get_usr, 'email': get_email}
                          )
    else:
        return render(request,
                      'accounts/after_register.html',
                      )

def resend_otp(request):
    if request.method == "GET":
        get_usr = request.GET['usr']
        if User.objects.filter(username = get_usr).exists() and not User.objects.get(username = get_usr).is_active:
            usr = User.objects.get(username=get_usr)
            # for otp with mail
            otp_with_mail(usr)

            return HttpResponse("Resend")

    return HttpResponse("Can't Send ")

def otp_with_mail(usr):
    usr_otp = random.randint(100000, 999999)
    UserOTP.objects.create(user=usr, otp=usr_otp)
    mess = f"Welcome to Soul Media\n\nHello {usr.first_name} {usr.last_name},\nYour Account Email verification OTP is {usr_otp}\n\nThanks!"

    send_mail(
        "Welcome to Soul Media - Verify Your Email",
        mess,
        'lujahawhsuk02@gmail.com',
        [usr.email],
        fail_silently=False
    )

def forget_password(request):
    return render(request,'password/password_reset_form.html')


@login_required
def profile(request):
    userinfo = UserInfo.objects.get(user=request.user)
    post = Post.objects.filter(author=request.user).order_by('-id')
    post_count = post.count()

    # follower or followings details
    following_obj = Following.objects.get(user=request.user)
    followers_count, followings_count = following_obj.follower.count(), following_obj.followed.count()
    followers = following_obj.follower.all()
    followeds = following_obj.followed.all()

    # saved post
    saved_post = Post.objects.filter(saved_post=request.user)
    saved_post_count = saved_post.count()

    context = {'userinfo':userinfo,'post': post,
               'post_count':post_count,
               'followers': followers,
               'followings': followeds,
               'follower_count': followers_count,
               'followings_count': followings_count,
               'saved_post':saved_post,
               'saved_post_count':saved_post_count,
               'profile_page':True}

    return render(request,'accounts/profile.html',context)

@login_required
def other_user_profile(request,username):
    if str(request.user.username) == str(username):
        return redirect('profile')

    user_d = User.objects.get(username=username)
    # print(user_d)
    userinfo = UserInfo.objects.get(user = user_d)

    # post
    post = Post.objects.filter(author=user_d).order_by('-id')
    post_count = post.count()

    # follower or followings details
    following_obj = Following.objects.get(user=user_d)
    # if following_obj is not None:
    followers_count, followings_count = following_obj.follower.count(), following_obj.followed.count()
    followers = following_obj.follower.all()
    followeds = following_obj.followed.all()

    # is following
    is_following = Following.objects.filter(user=request.user, followed=user_d)

    another_user = user_d

    if WhoProfileView.objects.filter(user=another_user,another_user=request.user).exists():
        print('j to hega')
        who = WhoProfileView.objects.get(user=another_user,another_user=request.user)
        print(who,who.user,who.another_user,who.created_at,who.count)
        who.count = who.count + 1
        who.created_at = datetime.datetime.now()
        who.save()
        # print(datetime.datetime.now())
    else:
        print('ni he')
        who = WhoProfileView(user=another_user,
                             another_user=request.user
                             )
        who.save()


    context = {'user_d' : user_d, 'userinfo' : userinfo,
               'post': post,
               'post_count' : post_count,
               'followers' : followers,
               'followings' : followeds,
               'follower_count' : followers_count,
               'followings_count' : followings_count,
               'is_following' : is_following
                }

    return render(request,'accounts/other_user_profile.html',context)


@login_required
def change_username(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.get(username = request.user)
        if User.objects.filter(username=username).exists():
            messages.error(request, 'username already exist..')
            print(username)
            return redirect('your_settings')
        else:
            user.username = username
            user.save()
            messages.success(request,'username changed successfully.')
            return redirect('your_settings')
    else:
        return render(request,'accounts/settings.html')

@login_required
def change_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.get(username = request.user)
        if User.objects.filter(email=email).exists():
            messages.error(request, 'email already exist..')
            print(email)
            return redirect('your_settings')
        else:
            user.email = email
            user.save()
            messages.success(request,'email changed successfully.')
            return redirect('your_settings')
    else:
        return render(request,'accounts/settings.html')


@login_required
def edit_account(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        website = request.POST['website']
        user_info = UserInfo.objects.get(user=request.user)
        request.user.first_name = firstname
        request.user.last_name = lastname
        request.user.save()
        print('user updated ')
        if user_info is not None:
            user_info.website = website
            user_info.save()
            messages.success(request,'information update successfully.')
            return redirect('your_settings')

    else:
        return render(request,'settings/settings.html')

@login_required
def edit_other_detail(request):
    user_info = UserInfo.objects.get(user=request.user)
    country = Country.objects.all()

    if request.method == 'POST':
        nickname = request.POST['nickname']
        gender = request.POST['gender']
        phone = request.POST['phone']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        if user_info is not None:
            user_info.nickname = nickname
            user_info.gender = gender
            user_info.phone = phone

            user_info.country = Country.objects.get(id=country)
            user_info.state= State.objects.get(id=state)
            user_info.city = City.objects.get(id=city)

            user_info.save()
            messages.success(request,'information update successfully.')
            return redirect('other_details')

    else:
        context={'userinfo':user_info,'country':country}
        return render(request,'settings/other_details.html',context)


@login_required
def change_profile_img(request):
    if request.method == 'POST':
        img = request.FILES.get('profile-img')

        user_info = UserInfo.objects.get(user=request.user)
        user_info.profile_photo = img
        user_info.save()
        messages.success(request,'change profile image successfully.')
        return redirect('your_settings')

    else:
        return render(request,'settings/settings.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        new_password2 = request.POST['new_password2']

        user = authenticate(username = request.user.username,password = old_password)

        if user == request.user:
            if new_password == new_password2:
                user.set_password(new_password)
                messages.success(request,'password change successfully.')
                return redirect('change_password')
            else:
                messages.error(request,'new & confirm password not match.')
                return redirect('change_password')
        else:
            messages.error(request, 'old password not match.')
            return redirect('change_password')

    else:
        return render(request,'settings/change_password.html')


from .forms import AddBioForm
def addBio(request):
    if request.method == 'POST':
        form = AddBioForm(request.POST)
        if form.is_valid():
            bio = form.cleaned_data['bio']
            user_info = UserInfo.objects.get(user=request.user)
            user_info.bio=bio
            user_info.save()
            return redirect('your_settings')
        else:
            return redirect('your_settings')


def user_logout(request):
    logout(request)
    return redirect('index')

def test(request):
    return render(request,'other/test.html')


@login_required()
def delete_account(request):
    u = User.objects.get(username = request.user.username)
    u.delete()
    return render(request,'other/delete_account_success.html')

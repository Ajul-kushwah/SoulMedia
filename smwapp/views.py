from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import ProfileView, UserInfo, Country, State, City, WhoProfileView
from accounts.forms import AddBioForm

from django.db.models import Q

# Create your views here.
from post.models import Following


def your_settings(request):
    user_info = UserInfo.objects.get(user=request.user)
    context={'user_info':user_info,'form':AddBioForm(request.POST or None,instance=user_info)}
    return render(request,'settings/settings.html',context)


def all_user(request):
    exclude_list = [request.user,'admin']
    user = User.objects.exclude(username__in=exclude_list)
    context = {'users':user,'user_count':user.count()}
    return render(request,'smwapp/all_user.html',context)


def all_suggest_user(request):
    following_obj = Following.objects.get(user=request.user)
    f =[request.user,'admin']
    for i in following_obj.followed.all():
        f.append(i.username)
    # print(f)
    suggest_user = User.objects.exclude(username__in=f)

    context = {'users':suggest_user,'user_count':suggest_user.count()}
    return render(request,'smwapp/all_suggest_user.html',context)


from django.db.models import Value as V
from django.db.models.functions import Concat


def search_user(request):
    if request.method == 'GET':
        q = request.GET.get('q')

        # users = User.objects.filter(username__icontains=q).exclude(username ='admin' )
        users = User.objects.annotate(
                        full_name=Concat('first_name', V(' '), 'last_name')
                    ).filter(
            Q(username__icontains=q) |
            Q(full_name__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        ).exclude(username ='admin' )


        context={'users':users,'user_count':users.count(),'query':q}
        return render(request,'search/search_user.html',context)



def push_notifications(request):
    return render(request,'settings/push_notifications.html')

@login_required
def other_details(request):
    user_info = UserInfo.objects.get(user=request.user)
    country = Country.objects.all()
    context={'userinfo':user_info,'country':country}
    return render(request,'settings/other_details.html',context)

@login_required
def privacy_and_security(request):
    return render(request,'settings/privacy_and_security.html')


def states_load(request):
    country_id = request.GET.get('countryId')
    states = State.objects.filter(country=country_id).order_by('name')
    # print(states)
    context={'states': states}
    return render(request, 'smwapp/states_list.html', context)

def city_load(request):
    state_id = request.GET.get('stateId')
    # city = City.objects.filter(state=State.objects.get(name=state_id)).order_by('name')
    city = City.objects.filter(state=state_id).order_by('name')

    context={'city': city}
    return render(request, 'smwapp/city_list.html', context)


def who_profile_view(request):
    who = WhoProfileView.objects.filter(user=request.user).order_by('-created_at')

    context = {'profile': who, 'user_count': who.count()}
    return render(request, 'smwapp/who_viewed_profile.html', context)





def userIndex(request):
    return render(request,'other/userIndex.html')

def userIndex2(request):
    return render(request,'other/userIndex2.html')

def insta_profile(request):
    return render(request,'other/profile_like_insta.html')



def error_404_view(request, exception):
    return render(request,'smwapp/error_404.html',status=404)
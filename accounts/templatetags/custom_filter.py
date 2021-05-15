from django import template
from post.models import Following
from django.contrib.auth.models import User
register = template.Library()

@register.filter(name='rupee')
def addRupeeSign(value):
    return f'₹ {value}'

from accounts.models import UserInfo

@register.filter(name='add_profile_image')
def addProfileImage(username):
    user_info = UserInfo.objects.get(user=username)
    return user_info.profile_photo.url

@register.filter(name='is_following')
def check_is_following(request,user):
    #check if already following
    to_follow = User.objects.get(username=user)
    following = Following.objects.filter(user=request.user, followed=to_follow)
    is_following = True if following else False
    return is_following


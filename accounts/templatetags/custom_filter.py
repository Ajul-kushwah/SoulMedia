from django import template

register = template.Library()

@register.filter(name='rupee')
def addRupeeSign(value):
    return f'₹ {value}'

from accounts.models import UserInfo

@register.filter(name='add_profile_image')
def addProfileImage(username):
    user_info = UserInfo.objects.get(user=username)
    return user_info.profile_photo.url
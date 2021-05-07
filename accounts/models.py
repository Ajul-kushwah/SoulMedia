from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class State(models.Model):
    country = models.ForeignKey(Country, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default='', related_name='user')
    profile_photo = models.ImageField(upload_to='profile_photo',default='default.png')
    nickname = models.CharField(max_length=10,blank=True, null=True)
    gender = models.CharField(max_length=10,blank=True, null=True)
    phone = models.CharField(max_length=10,blank=True, null=True)

    # country = models.CharField(max_length=100,blank=True, null=True)
    country = models.ForeignKey(Country,on_delete=models.SET_NULL,blank=True, null=True)
    # state = models.CharField(max_length=100,blank=True, null=True)
    state = models.ForeignKey(State,on_delete=models.SET_NULL,blank=True, null=True)
    # city = models.CharField(max_length=100,blank=True, null=True)
    city = models.ForeignKey(City,on_delete=models.SET_NULL,blank=True, null=True)

    website = models.URLField(default='')
    bio = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class WhoProfileView(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    another_user = models.ForeignKey(User,related_name="viewer",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user)


class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    time_st = models.DateTimeField(auto_now = True)
    otp = models.SmallIntegerField()
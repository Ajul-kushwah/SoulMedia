from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import os
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200 , blank=True , null=True)
    # image = models.ImageField(upload_to="post" ,default='', blank=True)
    image = models.FileField(upload_to="post" ,default='', blank=True)
    # body = models.TextField()
    body = RichTextField(blank=True, null=True)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')
    saved_post = models.ManyToManyField(User, default=None, blank=True, related_name='saved_post')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')

    def file_extension(self):
        name, extension = os.path.splitext(self.image.name)
        if extension == '.mp4':
            return 'mp4'
        else:
            return 'png'

    def __str__(self):
        return str(str(self.id) + ' ' + str(self.author))

    @property
    def num_likes(self):
        return self.liked.all().count()

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES , default='Like',max_length=10)

    def __str__(self):
        return str(self.post)


class Following(models.Model):
    """ Following of the user """
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    followed = models.ManyToManyField(User, related_name="followed",blank=True,null=True)
    follower = models.ManyToManyField(User, related_name="follower",blank=True,null=True)

    @classmethod
    def follow(cls, user, another_account):
        obj,create = cls.objects.get_or_create(user = user)
        obj.followed.add(another_account)

        obj,create = cls.objects.get_or_create(user = another_account)
        obj.follower.add(user)

    @classmethod
    def unfollow(cls, user, another_account):
        obj = cls.objects.get(user = user)
        obj.followed.remove(another_account)

        obj = cls.objects.get(user = another_account)
        obj.follower.remove(user)

    def __str__(self):
        return str(self.user)

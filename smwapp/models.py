from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stories(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    story = models.FileField(upload_to='stories',)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + " - " + str(self.created_at)


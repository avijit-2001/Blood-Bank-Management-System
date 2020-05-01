from django.db import models
from users.models import CustomUser
# Create your models here.

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_id = models.IntegerField(default=-1)
    post_id = models.IntegerField(default=-1)
    com = models.TextField(max_length=300)
    date_commented = models.DateTimeField(default=timezone.now)


class Reply(models.Model):
    user_id = models.IntegerField(default=-1)
    comment_id = models.IntegerField(default=-1)
    reply_to = models.TextField(max_length=300)
    date_commented = models.DateTimeField(default=timezone.now)


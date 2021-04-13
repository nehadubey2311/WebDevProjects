from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follows = models.ManyToManyField("self", symmetrical=False, related_name="followers")


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name="user_listings")
    content = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_by")

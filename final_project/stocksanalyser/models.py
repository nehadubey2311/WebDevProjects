from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name="user_posts")
    content = models.CharField(max_length=10000)
    category = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_by")
    approved = models.BooleanField(default=False)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name="user_questions")
    question = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)

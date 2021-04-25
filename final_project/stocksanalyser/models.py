from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    """
    User model
    """
    pass

class Category(models.Model):
    """
    Create categories to be assigned to articles
    """
    category = models.CharField(max_length=20)

class Article(models.Model):
    """
    Model to store articles
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name="user_posts")
    title = models.CharField(default=None, max_length=200)
    content = models.CharField(max_length=10000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None,
                                 blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    likes = models.ManyToManyField(User, blank=True, related_name="liked_by")
    approved = models.BooleanField(default=False)


class Question(models.Model):
    """
    Model to store questions asked by logged-in users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name="user_questions")
    question = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)


class Comment(models.Model):
    """
    Creates Comments model
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    comment = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)

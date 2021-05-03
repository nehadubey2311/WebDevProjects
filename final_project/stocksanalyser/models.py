from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    """
    User model
    """
    pass


class Article(models.Model):
    """
    Model to store articles
    """
    # Static category choices to be used as
    # blog menu items as well
    INVESTING = 'Investing'
    Learn_Tech_Analysis = 'tech_analysis'
    Learn_Fund_Analysis = 'fund_analysis'

    CATEGORY_CHOICES = [
        (INVESTING, 'Investing'),
        (Learn_Tech_Analysis, 'tech_analysis'),
        (Learn_Fund_Analysis, 'fund_analysis'),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=INVESTING,
        )

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name="user_posts")
    title = models.CharField(default=None, max_length=200)
    content = models.CharField(max_length=10000)
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
    answer = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """
    Creates Comments model
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    comment = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)

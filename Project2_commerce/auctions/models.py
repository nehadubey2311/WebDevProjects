from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Creates User model
    """

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    """
    Create categories to be assigned to listings
    """
    category = models.CharField(max_length=20)


class Listing(models.Model):
    """
    Creates Listing model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="user_listings", blank=True, null=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    bid = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    listing_image = models.URLField(default=None, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True,
                                null=True, related_name="list_category")
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_win",
                             default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.title} : starting bid {self.bid}, created on {self.created}"


class Bid(models.Model):
    """
    Creates Bids model
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    bid = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """
    Creates Comments model
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    comment = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)

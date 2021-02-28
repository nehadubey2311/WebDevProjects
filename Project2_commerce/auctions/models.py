from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Listings(models.Model):
    list_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings", blank=True, null=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    starting_bid = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    listing_image = models.URLField()
    category = models.CharField(max_length=20, default="any")

    def __str__(self):
        return f"{self.title} : starting bid {self.starting_bid}, created on {self.created}"


class Bids(models.Model):
    bid_list_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    bid_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.IntegerField
    time = models.TimeField


class Comments(models.Model):
    com_list_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    com_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    time = models.TimeField

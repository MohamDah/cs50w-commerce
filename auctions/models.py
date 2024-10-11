from django.contrib.auth.models import AbstractUser
from django.db import models


class listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    bid = models.IntegerField()
    image = models.URLField(null=True)
    category = models.CharField(max_length=64, null=True)
    seller = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.id}: {self.title}, starting bid: {self.bid}$"


class User(AbstractUser):
    watchlist = models.ManyToManyField(listings, blank=True, related_name="user_items")


class biddings(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bidded = models.ForeignKey(listings, on_delete=models.CASCADE, related_name="bids")
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.bidder}, {self.bidded.title}, {self.bid}$"

class winners(models.Model):
    winner = models.ForeignKey(biddings, on_delete=models.CASCADE, related_name="wins")

class comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    commented = models.ForeignKey(listings, on_delete=models.CASCADE, related_name="list_comments")
    comment = models.CharField(max_length=280)
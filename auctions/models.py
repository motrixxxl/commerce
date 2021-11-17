from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import *

class User(AbstractUser):
    pass


class Currency(models.Model):
    name = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self): 
        return f"{self.name}"


class Lot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lots')
    title = models.CharField(max_length=256)
    description = models.TextField()
    min_amount = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default='USD')
    image = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='lots')
    state = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def short_description(self):
        return truncate(self.description, 150, '')

    def __str__(self): 
        return f"{self.title} | {self.category}"


class Bet(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='bets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bets')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='watchlist')
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    lot = models.OneToOneField(Lot, on_delete=models.CASCADE, related_name='notification')
    type = models.IntegerField()
    state = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)



from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=256)


class Lot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lots')
    title = models.CharField(max_length=256)
    description = models.TextField()
    min_amount = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='lots')
    state = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Bet(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='bets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bets')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()
    created_at = models.DateTimeField()


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='watchlist')
    created_at = models.DateTimeField()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    lot = models.OneToOneField(Lot, on_delete=models.CASCADE, related_name='notification')
    type = models.IntegerField()
    state = models.IntegerField()
    created_at = models.DateTimeField()



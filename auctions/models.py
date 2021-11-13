from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Lot(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=256)
    description = models.TextField()
    min_amount = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.CharField(max_length=256)
    category_id = models.IntegerField(max_length=3)
    state = models.IntegerField(max_length=3)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Bet(models.Model):
    lot_id = models.IntegerField()
    user_id = models.IntegerField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField()


class Comment(models.Model):
    user_id = models.IntegerField()
    lot_id = models.IntegerField()
    message = models.TextField()
    created_at = models.DateTimeField()


class Watchlist(models.Model):
    user_id = models.IntegerField()
    lot_id = models.IntegerField()
    created_at = models.DateTimeField()


class Notifiction(models.Model):
    user_id = models.IntegerField()
    lot_id = models.IntegerField()
    type = models.IntegerField(max_length=3)
    state = models.IntegerField(max_length=3)
    created_at = models.DateTimeField()


class Category(models.Model):
    name = models.CharField(max_length=256)
    lots = mo

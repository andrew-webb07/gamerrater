from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150)
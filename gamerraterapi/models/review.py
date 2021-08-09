from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    review = models.CharField(max_length=200)
    player = models.ForeignKey("Player", on_delete=CASCADE)
    game = models.ForeignKey("Game", on_delete=CASCADE)
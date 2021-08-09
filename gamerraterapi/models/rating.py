from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator

class Rating(models.Model):
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(10), MinValueValidator(1)])
    player = models.ForeignKey("Player", on_delete=CASCADE)
    game = models.ForeignKey("Game", on_delete=CASCADE)
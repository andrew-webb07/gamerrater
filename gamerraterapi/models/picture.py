from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator

class Picture(models.Model):
    image = models.ImageField(upload_to="image", height_field=None, width_field=None, max_length=None, null=True)
    player = models.ForeignKey("Player", on_delete=CASCADE)
    game = models.ForeignKey("Game", on_delete=models.DO_NOTHING, related_name='pictures')
from django.db import models
from django.db.models.deletion import CASCADE
from .rating import Rating

class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    designer = models.CharField(max_length=50)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    estimated_time_to_play = models.DurationField()
    age_recommendation = models.IntegerField()
    categories = models.ManyToManyField("Category", through="GameCategory", related_name="categories")
    
    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = Rating.objects.filter(game=self)

        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating
        
        if total_rating == 0:
            return 0
        else:
            average_rating = total_rating / len(ratings)
            return average_rating
"""View module for handling requests about ratings"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from gamerraterapi.models import Rating, Player, Game
from django.contrib.auth.models import User


class RatingView(ViewSet):
    """Level up ratings"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single rating

        Returns:
            Response -- JSON serialized rating
        """
        try:
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all ratings

        Returns:
            Response -- JSON serialized list of ratings
        """
        ratings = Rating.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = RatingSerializer(
            ratings, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized rating instance
        """
        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["gameId"])
        rating = Rating()
        rating.rating = request.data["rating"]
        rating.player = player
        rating.game = game
        
        try:
            rating.save()
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class RatingUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = RatingUserSerializer(many=False)

    class Meta:
        model = Player
        fields = ['user', 'bio']

class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for ratings

    Arguments:
        serializers
    """
    player = PlayerSerializer(many=False)

    class Meta:
        model = Rating
        fields = ('id', 'rating', 'player', 'game')
        depth = 1
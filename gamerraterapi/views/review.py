"""View module for handling requests about Reviews"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from gamerraterapi.models import Review, Player, Game
from django.contrib.auth.models import User


class ReviewView(ViewSet):
    """Level up Reviews"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Review

        Returns:
            Response -- JSON serialized Review
        """
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all Reviews

        Returns:
            Response -- JSON serialized list of Reviews
        """
        reviews = Review.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Review instance
        """
        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["gameId"])
        review = Review()
        review.review = request.data["review"]
        review.player = player
        review.game = game
        
        try:
            review.save()
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class ReviewUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = ReviewUserSerializer(many=False)

    class Meta:
        model = Player
        fields = ['user', 'bio']

class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for Reviews

    Arguments:
        serializers
    """
    player = PlayerSerializer(many=False)

    class Meta:
        model = Review
        fields = ('id', 'review', 'player', 'game')
        depth = 1
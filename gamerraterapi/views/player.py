"""View module for handling requests about Players"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from gamerraterapi.models import Player
from django.contrib.auth.models import User


class PlayerView(ViewSet):
    """Level up Players"""

    def list(self, request):
        """Handle GET requests to Players resource
        
        Returns JSON serialized list of Players
        """
        players = Player.objects.all()
        serializer = PlayerSerializer(
            players, many=True, context={'request': request})
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = UserSerializer(many=False)

    class Meta:
        model = Player
        fields = ['id', 'user', 'bio']

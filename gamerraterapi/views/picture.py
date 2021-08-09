"""View module for handling requests about pictures"""

# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gamerraterapi.models import Game, Picture, Player

class PictureView(ViewSet):
    def create(self, request):
        """Handle POST operations for pictures

        Returns:
            Response -- JSON serialized picture instance
        """

        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(user=request.data["gameId"])
        picture = Picture()
        picture.image = request.data["image"]
        picture.player = player
        picture.game = game

        try:
            picture.save()
            serializer = PictureSerializer(picture, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single picture

        Returns:
            Response -- JSON serialized picture instance
        """
        try:
            picture = Picture.objects.get(pk=pk)
            serializer = PictureSerializer(picture, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(user=request.data["gameId"])

        picture = Picture.objects.get(pk=pk)
        picture.id = request.data["pictureId"]
        picture.image = request.data["image"]
        picture.player = player
        picture.game = game

        picture.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            picture = Picture.objects.get(pk=pk)
            picture.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Picture.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to pictures resource

        Returns:
            Response -- JSON serialized list of pictures
        """

        pictures = Picture.objects.all()


        serializer = PictureSerializer(
            pictures, many=True, context={'request': request})
        return Response(serializer.data)

class PictureSerializer(serializers.ModelSerializer):
    """JSON serializer for pictures

    Arguments:
        serializer type
    """
    class Meta:
        model = Picture
        fields = ('id', 'image', 'player', 'game')
        depth = 1

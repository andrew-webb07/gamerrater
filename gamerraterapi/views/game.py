"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.db.models import Q
from gamerraterapi.models import Game, Category
import datetime

class GameView(ViewSet):
    """Gamer Rater Games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        game = Game()
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.year_released = request.data["yearReleased"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.estimated_time_to_play = datetime.timedelta(hours=request.data["estimatedTimeToPlay"])
        game.age_recommendation = request.data["ageRecommendation"]

        try:
            game.save()
            game.categories.set(request.data["categories"])
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.year_released = request.data["yearReleased"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.estimated_time_to_play = datetime.timedelta(hours=request.data["estimatedTimeToPlay"])
        game.age_recommendation = request.data["ageRecommendation"]
        game.categories.set([category["id"] for category in request.data["categories"]])
        game.save()
        

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """


        games = Game.objects.all()

        search_text = self.request.query_params.get('q', None)

        if search_text is not None:
            games = Game.objects.filter(
                    Q(title__contains=search_text) |
                    Q(description__contains=search_text) |
                    Q(designer__contains=search_text)
)
        sort_text = self.request.query_params.get('orderby', None)

        if sort_text is not None:
            games = Game.objects.order_by(sort_text)

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)

#     def search(self, request):
#         """Handle GET requests to games resource

#         Returns:
#             Response -- JSON serialized list of games
#         """
#         search_text = self.request.query_params.get('q', None)

#         games = Game.objects.filter(
#                 Q(title__contains=search_text) |
#                 Q(description__contains=search_text) |
#                 Q(designer__contains=search_text)
# )

#         serializer = GameSerializer(
#             games, many=True, context={'request': request})
#         return Response(serializer.data)

    # def sort(self,request):
    #     """Handle GET requests to games resource

    #     Returns:
    #         Response -- JSON serialized list of games
    #     """
    #     sort_text = self.request.query_params.get('q', None)

    #     games = Game.objects.order_by(sort_text)

    #     serializer = GameSerializer(
    #         games, many=True, context={'request': request})
    #     return Response(serializer.data)        


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'year_released','number_of_players', 'estimated_time_to_play', 'age_recommendation', 'categories', 'average_rating')
        depth = 1

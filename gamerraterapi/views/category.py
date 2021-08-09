from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gamerraterapi.models import Category

class CategoryView(ViewSet):
    def list(self, request):
        """Handle GET requests to categories resource

        Returns:
            Response -- JSON serialized list of categories
        """
        categories = Category.objects.all()

        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories

    Arguments:
        serializer type
    """
    class Meta:
        model = Category
        fields = ('id', 'label')
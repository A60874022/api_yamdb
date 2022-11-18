from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg

from reviews.models import Comment, Review, Titles


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')


class TitlesSerializer(serializers.ModelSerializer):
    """Класс ввода/вывода данных в заданном формате для модели Titles"""
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category', 'rating')
        model = Titles

    def get_rating(self, obj):
        try:
            rating = obj.reviews.aggregate(Avg('score'))
            return rating.get('score__avg')
        except TypeError:
            return None

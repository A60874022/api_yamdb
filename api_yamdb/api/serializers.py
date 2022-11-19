from rest_framework import serializers

from rest_framework.relations import SlugRelatedField
from django.db.models import Avg
from reviews.models import Categories, Genres, Titles, Comment, Review, Titles


class CategoriesSerializer(serializers.ModelSerializer):
    """"Класс ввода/вывода данных в заданном формате для модели Categories"""
   
    class Meta:
        fields = ('id', 'name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    """Класс ввода/вывода данных в заданном формате для модели Genres"""


    class Meta:
        fields = ('id', 'name', 'slug')
        model = Genres


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
    Genre = serializers.StringRelatedField()
    Categories = serializers.StringRelatedField(many=True)
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

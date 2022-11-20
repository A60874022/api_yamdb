from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg

from reviews.models import Categories, Genres, Titles, Comment, Review, Titles
from reviews.models import User

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

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_username(self, value):
        username = value.lower()
        if username == "me":
            raise serializers.ValidationError("Имя me недоступно")
        return value

    class Meta:
        model = User
        fields = ('username', 'email')

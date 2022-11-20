from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg

from reviews.models import Categories, Genres, Titles, Comment, Review, Titles, User


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
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Categories.objects.all())
       
    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating')
        model = Titles


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()

    class Meta:
        model = Titles
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Username 'me' is not valid")
        return value

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

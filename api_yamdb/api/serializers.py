from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from users.models import User

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """"Класс ввода/вывода данных в заданном формате для модели Category"""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Класс ввода/вывода данных в заданном формате для модели Genre"""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CommentSerializer(serializers.ModelSerializer):
    """Класс ввода/вывода данных в заданном формате для модели Comment"""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UniqueTitle:
    requires_context = True

    def __init__(self, context_key):
        self.key = context_key

    def __call__(self, serializer_field):
        return serializer_field.context.get('view').kwargs.get(self.key)

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class ReviewSerializer(serializers.ModelSerializer):
    """Класс ввода/вывода данных в заданном формате для модели Review"""
    author = SlugRelatedField(slug_field='username',
                              default=serializers.CurrentUserDefault(),
                              read_only=True)
    title = serializers.HiddenField(
        default=UniqueTitle('title_id'))

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date', 'title')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author']
            )
        ]


class TitleSerializer(serializers.ModelSerializer):
    """Класс вывода данных в заданном формате для модели Title"""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category',)
        model = Title


class ReadOnlyTitleerializer(serializers.ModelSerializer):
    """Класс ввода данных в заданном формате для модели Title"""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score'))['score__avg']
        return rating


class RegistrationSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        username = value.lower()
        if username.lower() == 'me':
            raise serializers.ValidationError('Имя me недоступно')
        return value

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    """Класс ввода данных в заданном формате Токена"""
    username = serializers.CharField(
        required=True,
        max_length=15,
    )
    confirmation_code = serializers.CharField(
        required=True,
        max_length=150
    )


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'bio',
                  'first_name',
                  'last_name',
                  'role')


class UsersChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'bio',
                  'first_name',
                  'last_name',
                  'role')
        read_only_fields = ('role',)

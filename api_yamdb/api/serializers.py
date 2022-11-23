from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


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


class Titleerializer(serializers.ModelSerializer):
    """Класс ввода/вывода данных в заданном формате для модели Title"""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        model = Title


class ReadOnlyTitleerializer(serializers.ModelSerializer):
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


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=15,
    )
    confirmation_code = serializers.CharField(
        required=True,
        max_length=150
    )


class AdminUsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'bio',
                  'first_name',
                  'last_name',
                  'role')


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'bio',
                  'first_name',
                  'last_name',
                  'role')


class UsersChangeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'bio',
                  'first_name',
                  'last_name',
                  'role')
        read_only_fields = ('role',)

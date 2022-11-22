from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title, Comment, Review, User


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
        fields = ('text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')


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
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


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

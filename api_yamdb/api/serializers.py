from rest_framework import serializers

from reviews.models import Categories, Genres, Titles


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


class TitlesSerializer(serializers.ModelSerializer):
    """Класс ввода/вывода данных в заданном формате для модели Titles"""
    genre = serializers.StringRelatedField(many=True, read_only=True)
    category = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
        model = Titles


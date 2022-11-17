from django.contrib.auth import get_user_model
from django.db import models



class Categories(models.Model):
    """Класс для создания таблицы Categories"""
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    titles = models.ForeignKey('Titles', on_delete=models.PROTECT)

class Genres(models.Model):
    """Класс для создания таблицы Genres"""
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    titles = models.ForeignKey('Titles', on_delete=models.PROTECT)


class Titles(models.Model):
    """Класс для создания таблицы Title"""
    name =  models.CharField(max_length=256)
    year = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=256)
    genre = models.ManyToManyField(Genres, through='GenresTitles')
    category = models.OneToOneField(Categories, through='CategoriesTitles')
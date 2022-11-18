from django.contrib.auth import get_user_model
from django.db import models



class Categories(models.Model):
    """Класс для создания таблицы Categories"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
 

class Genres(models.Model):
    """Класс для создания таблицы Genres"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
 


class Titles(models.Model):
    """Класс для создания таблицы Title"""
    name =  models.CharField(max_length=256)
    year = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=256)
    genre = models.ManyToManyField(Genres, through='GenresTitles')
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)

class GenresTitles(models.Model):
    Genres = models.ForeignKey(
        Genres, on_delete=models.CASCADE)
    Titles = models.ForeignKey(
        Titles, on_delete=models.CASCADE)
from django.contrib.auth import get_user_model
from django.db import models

class Categories(models.Model):
    """Класс для создания таблицы Categories"""
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

class Genres(models.Model):
    """Класс для создания таблицы Genresgit """
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
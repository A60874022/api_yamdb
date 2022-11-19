from django.contrib.auth import get_user_model
from django.db import models

from .validate import validate_year
from django.core.validators import MaxValueValidator, MinValueValidator

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
    year = models.IntegerField(blank=True, null=True, validators=[validate_year])
    description = models.CharField(max_length=256)
    genre = models.ManyToManyField(Genres, through='GenresTitles')
    Categories = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, related_name='Categories')


class GenresTitles(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=256)
    genre = models.ManyToManyField(Genres, through='GenresTitles')
    category = models.OneToOneField(Categories, through='CategoriesTitles')
    rating = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Класс для создания отзыва на произведение"""
    title = models.ForeignKey(Titles, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField(verbose_name='Отзыв', help_text='Напишите отзыв')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(10)])

    class Meta:
        ordering = ('-pub_date', 'score')
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review')
        ]


class Comment(models.Model):
    """Класс для создания комментария к отзыву"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(verbose_name='Комментарий',
                            help_text='Введите текст комментария')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pub_date',)

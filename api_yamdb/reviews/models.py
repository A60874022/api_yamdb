from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validate import validate_year
from users.models import User


class Сommon(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True


class Category(Сommon):
    """Класс для создания таблицы Category"""
    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(Сommon):
    """Класс для создания таблицы Genre"""
    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Класс для создания таблицы Title"""
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения',
                            help_text='Укажите название произведения')
    year = models.IntegerField(blank=True, null=True,
                               validators=[validate_year])
    description = models.CharField(max_length=256, verbose_name='Описание')
    genre = models.ManyToManyField(Genre, through='GenreTitles',
                                   verbose_name='Жанр')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='Category')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                              MaxValueValidator(10)],
                                              blank=True,
                                              null=True,
                                              verbose_name='Категория')

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitles(models.Model):
    """Класс для настройки пользователей Genrе"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Review(models.Model):
    """Класс для создания отзыва на произведение"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Произведение')
    text = models.TextField(verbose_name='Отзыв', help_text='Напиши отзыв')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор отзыва')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True,
                                    verbose_name='Дата публикации')
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                             MaxValueValidator(10)],
                                             verbose_name='Оценка')

    class Meta:
        ordering = ('-pub_date', 'score')
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review')
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


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
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text

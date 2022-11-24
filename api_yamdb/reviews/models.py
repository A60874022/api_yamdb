from django.db import models
from .validate import validate_year
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db import models


class Category(models.Model):
    """Класс для создания таблицы Category"""
    name = models.CharField(max_length=256,
                            verbose_name='Название категории',
                            help_text='Укажите название для категории')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Класс для создания таблицы Genre"""
    name = models.CharField(max_length=256,
                            verbose_name='Название жанра',
                            help_text='Укажите название жанра')
    slug = models.SlugField(unique=True)

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
                               validators=[validate_year],
                               verbose_name='Год выпуска',
                               help_text='Задайте год выпуска')
    description = models.CharField(max_length=256, verbose_name='Описание')
    genre = models.ManyToManyField(Genre, through='GenreTitles',
                                   verbose_name='Жанр')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='Category',
                                 verbose_name='Категория')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                              MaxValueValidator(10)])

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitles(models.Model):
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
    text = models.TextField(verbose_name='Отзыв', help_text='Напишите отзыв')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор отзыва')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True,
                                    verbose_name='Дата публикации')
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(10)],
                                             verbose_name='Оценка')

    class Meta:
        ordering = ('-pub_date', 'score')
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review')
        ]

    def __str__(self):
        return self.text[:15]


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

    def __str__(self):
        return self.text[:15]

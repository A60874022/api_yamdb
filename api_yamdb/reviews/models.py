from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """"Выбор роли для пользователя"""
    CHOICES = (
        ('admin', 'Админ'),
        ('moderator', 'Модер'),
        ('user', 'Подтвержденный пользователь'),
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        choices=CHOICES,
        max_length=30,
        default='U'
    )
    confirmation_code = models.CharField(
        blank=True,
        max_length=150
    )

    def __str__(self):
        return self.username

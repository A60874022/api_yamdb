from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """"Выбор роли для пользователя"""
    CHOICES = (
        ('A', 'Админ'),
        ('M', 'Модер'),
        ('U', 'Подтвержденный пользователь'),
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

    def __str__(self):
        return self.username

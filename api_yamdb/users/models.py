from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    CHOICES = (
        (ADMIN, 'Админ'),
        (MODERATOR, 'Модер'),
        (USER, 'Подтвержденный пользователь'),
    )
    username = models.CharField(
        'Имя',
        max_length=30,
        unique=True,
        null=False,
        blank=False,
    )
    email = models.EmailField(
        'эмеил',
        unique=True,
        blank=False,
        null=False,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        choices=CHOICES,
        max_length=30,
        default=USER
    )
    confirmation_code = models.CharField(
        blank=True,
        max_length=150
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_staff

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return self.username

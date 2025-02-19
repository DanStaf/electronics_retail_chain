from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='Почта', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):

        if self.first_name and self.last_name:
            return f'USER: {self.first_name} {self.last_name}'
        else:
            return f'USER: {self.email}'

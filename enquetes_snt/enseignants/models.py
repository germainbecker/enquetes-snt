from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # custom User pour rendre l'adresse mail unique
    email = models.EmailField(
        verbose_name="email",
        max_length=60,
        unique=True,
        error_messages={
            'unique': "Un compte existe déjà pour cette adresse email.",
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'last_name', 'first_name']


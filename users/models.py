from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomsUser(AbstractUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to="photo/avatars/", blank=True, null=True)

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)
    country = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Страна",
        help_text="Укажите страну",
    )
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]
        permissions = [
            ("can_manage_users", "can manage users"),
            ("can_block_users", "can block users"),
        ]

    def __str__(self):
        return self.email

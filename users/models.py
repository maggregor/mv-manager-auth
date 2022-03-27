from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.management.utils import get_random_secret_key


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner_email = models.EmailField()

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, db_index=True)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    access_token = models.CharField(max_length=2048, null=True, blank=True)
    picture = models.CharField(max_length=2048, null=True, blank=True)
    secret_key = models.CharField(max_length=255, default=get_random_secret_key)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, null=True, blank=True, to_field="name"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        swappable = "AUTH_USER_MODEL"

    @property
    def name(self):
        if not self.last_name:
            return self.first_name.capitalize()

        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

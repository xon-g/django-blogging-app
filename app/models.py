from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class AbstractBaseModel(models.Model):
    """Abstract base class that adds created_at and updated_at fields to models."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractUser, AbstractBaseModel):

    class Meta:
        db_table = 'auth_user'

        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['last_login']),
            models.Index(fields=['date_joined']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['created_at'])
        ]


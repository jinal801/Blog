from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# Create your models here.
class User(AbstractUser):
    """
    create user registration model using abstract user
    """

    class Meta:
        ordering = ['id']
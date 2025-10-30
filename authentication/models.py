from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Make email unique for login purposes
    email = models.EmailField(unique=True)

    # You can optionally override first_name, last_name if you want blank=True
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    # date_joined already exists in AbstractUser, so you can remove this line unless you need customization
    # date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

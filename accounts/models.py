from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)  # unique email enforced

    # Optional: you can force username to be optional and use email as login
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']  

    def __str__(self):
        return self.username

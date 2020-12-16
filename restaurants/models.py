from django.contrib.auth.models import AbstractUser
from django.db import models

# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class User(AbstractUser):
    pass



# After changing anything here:
    # python3 manage.py makemigrations
    # python3 manage.py migrate
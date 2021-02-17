from django.contrib.auth.models import AbstractUser
from django.db import models

# https://www.reddit.com/r/django/comments/llb98f/arraylist_as_model_field/
class Restaurant(models.Model):
    name = models.CharField(max_length=500)
    regular_id = models.CharField(max_length=500)
    details_id = models.CharField(max_length=500)

# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class User(AbstractUser):
    saved_restaurants = models.ManyToManyField(Restaurant, blank=True)


# After changing anything here:
    # python3 manage.py makemigrations
    # python3 manage.py migrate
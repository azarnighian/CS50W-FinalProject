from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("results", views.results, name="results"),
    path("testing", views.testing, name="testing")
]
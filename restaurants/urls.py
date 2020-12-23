from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("results/<str:city>", views.results, name="results"),
    path("restaurant/<str:name>/<str:id>", views.restaurant_details, name="restaurant")
]
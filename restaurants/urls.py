from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("about", views.about, name="about"),
    path("results", views.results, name="results"),
    path("results/<str:city>", views.results, name="results"),
    path("results/<str:city>/<int:radius>", views.results, name="results"),
    path("results/<str:city>/<str:categories>", views.results, name="results"),
    path("results/<str:city>/<int:radius>/<str:categories>", views.results, name="results"),
        # https://docs.djangoproject.com/en/3.1/topics/http/urls/#specifying-defaults-for-view-arguments
    path("restaurant/<str:name>/<str:id>/<str:details_id>", views.restaurant_page, name="restaurant_page"),
    path("add_or_remove/<str:add_or_remove>/<str:regular_id>/<str:details_id>", views.add_or_remove, name="add_or_remove"),
    path("get_categories", views.get_categories, name="get_categories")
]
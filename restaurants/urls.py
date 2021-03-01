from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("about", views.about, name="about"),
    path("results/<str:city>/<str:filters>/<int:radius>/<str:keyword>/<int:min_price>/<int:max_price>", views.results, name="results"),
    path("restaurant/<str:name>/<str:id>/<str:details_id>", views.restaurant_page, name="restaurant_page"),
    path("add_or_remove/<str:add_or_remove>/<str:regular_id>/<str:details_id>", views.add_or_remove, name="add_or_remove")
]
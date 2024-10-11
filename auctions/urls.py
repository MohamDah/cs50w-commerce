from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:TITLE>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove", views.remove, name="remove"),
    path("bid", views.bid, name="bid"),
    path("close", views.close, name="close"),
    path("comments", views.comment, name="comments"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.cat, name="cat")
]

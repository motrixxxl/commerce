from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("lot/<int:lot_id>", views.lot, name="lot"),
    path("bid/<int:lot_id>", views.bid, name="bid"),
    path("comment/<int:lot_id>", views.comment, name="comment"),
    path("watchlist/<int:lot_id>", views.watchlist, name="watchlist"),
    path("lot", views.addlot, name="addlot"),
]

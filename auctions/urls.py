from django.conf import settings
from django.conf.urls.static import static
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
    path("watchlist/<int:lot_id>", views.addwatchlist, name="addwatchlist"),
    path("lot", views.addlot, name="addlot"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("lots", views.mylots, name="mylots"),
    path("close/<int:lot_id>", views.close, name="close"),
    path("bids", views.mybids, name="mybids"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("read", views.read, name="read"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

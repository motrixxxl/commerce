from django.contrib import admin

from .models import Comment, Watchlist, Lot, Notification, User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    # list_display = ("id", "origin", "destination", "duration")
    pass

class WatchlistAdmin(admin.ModelAdmin):
    # filter_horizontal = ("flights",)
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Notification)
admin.site.register(Lot)

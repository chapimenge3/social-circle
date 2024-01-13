from django.contrib import admin

from .models import FriendRequest, Friends


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "friend", "is_accepted", "created_at", "updated_at")
    list_filter = ("user", "friend", "is_accepted", "created_at", "updated_at")
    search_fields = ("user", "friend")
    list_per_page = 25


class FriendsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "friend", "accepted_at", "created_at", "updated_at")
    list_filter = ("user", "friend", "accepted_at", "created_at", "updated_at")
    search_fields = ("user", "friend")
    list_per_page = 25

admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Friends, FriendsAdmin)

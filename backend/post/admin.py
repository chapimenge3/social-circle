from django.contrib import admin

from .models import Post, Comment, Like


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "body", "created_at", "updated_at")
    list_filter = ("author", "created_at", "updated_at")
    search_fields = ("author", "body")
    list_per_page = 25


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "body", "created_at", "updated_at")
    list_filter = ("author", "post", "created_at", "updated_at")
    search_fields = ("author", "post", "body")
    list_per_page = 25


class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "liker", "post", "created_at", "updated_at")
    list_filter = ("liker", "post", "created_at", "updated_at")
    search_fields = ("liker", "post")
    list_per_page = 25


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)

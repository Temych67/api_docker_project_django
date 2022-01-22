from django.contrib import admin
from main_app.models import Post, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "creation_date")


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "creation_date")


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

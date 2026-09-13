from django.contrib import admin
from .models import Category,Post,Comment
admin.site.register(Category)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=("title","author","category","status","views","created_at")
    list_filter=("status","category")
    search_fields=("title","content","author__username")
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=("post","user","created_at")

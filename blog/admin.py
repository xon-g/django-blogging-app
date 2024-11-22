from django.contrib import admin
from blog.models import Author, Post, Comment

# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'updated_at')
    readonly_fields = ('name', 'email', 'created_at', 'updated_at')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'author', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'body', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')



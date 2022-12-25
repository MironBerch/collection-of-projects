from django.contrib import admin
from api.models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',), }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'date_created', 'posted')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_per_page = 30
    prepopulated_fields = {'slug': ('title',), }
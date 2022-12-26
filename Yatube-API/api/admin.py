from django.contrib import admin
from api.models import Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin class"""
    list_display = ('pk', 'image', 'publish_date', 'author', 'group')
    search_fields = ('text',)
    empty_value_display = '-Пусто-'
    list_filter = ('publish_date',)
    

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Group admin class"""
    list_display = ('title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = '-Пусто-'
    list_filter = ('title',)
    search_fields = ('slug',)
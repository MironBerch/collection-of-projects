from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from .models import *


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    prepopulated_fields = {'slug': ('title',)}
    save_as = True
    save_on_top = True
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('category', 'tags')
    readonly_fields = ('views', 'create_at', 'get_photo')
    fields = ('title', 'slug', 'category', 'tags', 'content', 'photo', 'views', 'create_at',)
    list_display = ('id', 'title', 'slug', 'category', 'create_at', 'get_photo')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        else:
            return '-'
    get_photo.short_description = 'Фото'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
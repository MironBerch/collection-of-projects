from django.contrib import admin
from socialnetwork.models import Post, Profile, LikePost, FollowersCount
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *



admin.site.register(LikePost)
admin.site.register(FollowersCount)


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    readonly_fields = ('user', 'bio', 'get_photo')
    list_display = ('user', 'id_user', 'bio', 'get_photo')

    def get_photo(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50">')
        else:
            return '-'
    get_photo.short_description = 'Фото'


class PostAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display_links = ('id', 'text')
    search_fields = ('text', 'caption')
    list_filter = ('likes',)
    readonly_fields = ('likes', 'create_at', 'get_photo')
    list_display = ('id', 'text', 'caption', 'create_at', 'get_photo')

    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50">')
        else:
            return '-'
    get_photo.short_description = 'Фото'


admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
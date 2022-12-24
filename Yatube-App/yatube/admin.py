from django.contrib import admin
from yatube.models import Comment, Follow, Group, Post


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin class"""
    list_display = ('pk', 'post', 'author', 'text', 'created',)
    list_editable = ('author',)
    list_filter = ('author',)
    list_per_page = 10
    search_fields = ('text',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Follow admin class"""
    list_display = ('pk', 'author', 'user')
    list_editable = ('author',)
    list_filter = ('author',)
    list_per_page = 10
    search_fields = ('author',)
    

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Group admin class"""
    list_display = ('pk', 'title', 'slug', 'description', 'count_posts')
    empty_value_display = '-Пусто-'
    list_filter = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    
    def count_posts(self, object):
        return object.posts.count()

    count_posts.short_description = 'Колличество записей'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin class"""
    list_display = ('pk', 'text', 'image', 'publish_date', 'author', 'group', 'count_comments')
    empty_value_display = '-Пусто-'
    list_editable = ('group',)
    list_filter = ('publish_date',)
    list_per_page = 10
    search_fields = ('text',)

    def count_comments(self, object):
        return object.comments.count()

    count_comments.short_description = 'Колличество комментариев'
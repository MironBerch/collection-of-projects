from django import template
from blog.models import Post, Tag


register = template.Library()


@register.inclusion_tag('blog/most_popular_posts.html')
def get_most_popular_posts(cnt=3):
    posts = Post.objects.order_by('-views')[:cnt]
    return {"posts": posts}


@register.inclusion_tag('blog/tags_cloud.html')
def get_tags():
    tags = Tag.objects.all()
    return {"tags": tags}
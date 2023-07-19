from django.db import models

from accounts.models import User
from posts.managers import PostManager


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    content = models.TextField(
        blank=True,
        max_length=2500,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    is_reply = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    liked = models.ManyToManyField(
        User,
        blank=True,
        related_name='liked',
    )
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='alt',
    )

    objects = PostManager.as_manager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        ellipsis = '...' if len(self.content) > 100 else ''
        return f'{self.content[:100]}{ellipsis}'

    def get_replies(self):
        """Get a post's replies."""
        return self.alt.filter(
            is_active=True,
            is_reply=True,
        ).order_by('created_at')

    def get_reposts(self):
        """Get a post's reposts."""
        return self.alt.filter(
            is_active=True,
            is_reply=False,
        ).order_by('created_at')

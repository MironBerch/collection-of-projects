from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """Post class."""
    text = models.TextField(verbose_name='запись', help_text='Пожалуйста, оставьте вашу запись')
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации', db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='автор')
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, related_name='posts', blank=True, null=True, verbose_name='сообщество', help_text='Пожалуйста, выберите вашу группу')
    image = models.ImageField(upload_to='posts/', blank=True, verbose_name='изображение')

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ('-publish_date',)

    def __str__(self):
        return self.text


class Group(models.Model):
    """Group class."""
    title = models.CharField(max_length=200, verbose_name='Название сообщества', db_index=True)
    slug = models.SlugField(unique=True, verbose_name='адресс')
    description = models.TextField(verbose_name='описание')

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'
        ordering = ('title',)


    def __str__(self):
        return self.title


class Comment(models.Model):
    """Coment class."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='запись')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='автор')
    text = models.TextField(verbose_name='комментарий', help_text='Пожалуйста, оставьте ваш комментарий')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации', db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return self.text



class Follow(models.Model):
    """Author following class."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower', verbose_name='подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', verbose_name='автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('author',)

        constraints = (models.UniqueConstraint(fields=['author', 'user'], name='unique_follow'),)
from django.db import models
from datetime import datetime
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=55)
    slug = models.SlugField(
        max_length=55, verbose_name='Url', unique=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=55, unique=True)
    content = models.TextField()
    slug = models.SlugField(
        max_length=55, verbose_name='Url', unique=True
    )
    posted = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='posts'
    )
    preview_image = models.ImageField(upload_to='preview_image/%Y/%m/%d/')
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']
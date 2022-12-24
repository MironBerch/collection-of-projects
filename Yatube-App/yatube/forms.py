from django import forms
from yatube.models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreationForm(UserCreationForm):
    """User registration form"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PostForm(forms.ModelForm):
    """Post creation form"""
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm):
    """Comment creation form"""
    class Meta:
        model = Comment
        fields = ('text',)
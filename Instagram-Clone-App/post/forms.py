from django import forms
from post.models import Post


class NewPostForm(forms.ModelForm):
    content = forms.FileField(widget=forms.ClearableFileInput(attrs={'mltiple': True}), required=True)
    caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'c;lass': 'input is-medium'}), required=True)

    class Meta:
        model = Post
        fields = ('content', 'caption', 'tags')
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from foodgram.models import Recipe
from django.forms import ModelForm


class CreationForm(UserCreationForm):
    """Registretion form"""
    def __init__(self, *args, **kwargs):
        super(CreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email')
        required_fields = ('first_name', 'username', 'email')


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'time', 'description', 'image')

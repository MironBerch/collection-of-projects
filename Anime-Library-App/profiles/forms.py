from django import forms

from profiles.models import Profile, ProfileComment


class ProfileForm(forms.ModelForm):
    """Form for change profile settings"""

    birthday = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        ),
        required=False,
    )

    class Meta:
        model = Profile
        fields = ('profile_image', 'birthday', 'gender', 'description',)



class ProfileCommentForm(forms.ModelForm):
    """Form for send profile comment"""

    class Meta:
        model = ProfileComment
        fields = ('content',)
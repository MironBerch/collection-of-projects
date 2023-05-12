from django import forms


class SignupForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(),
        max_length=100,
        required=True,
    )
    name = forms.CharField(
        widget=forms.TextInput(),
        max_length=100,
        required=True,
    )
    surname = forms.CharField(
        widget=forms.TextInput(),
        max_length=100,
        required=True,
    )
    patronymic = forms.CharField(
        widget=forms.TextInput(),
        max_length=100,
        required=False,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        max_length=100,
        required=True,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        max_length=100,
        required=True,
    )

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            self._errors['password'] = self.error_class(
                ['Пароли не совпадают.'],
            )
        return self.cleaned_data


class SigninForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(),
        max_length=100,
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        max_length=100,
        required=True,
    )

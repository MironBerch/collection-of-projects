from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserChangeForm,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile, User
from accounts.tasks import send_password_reset_code
from schools.models import Class, School


class SignUpForm(UserCreationForm):
    """Form for signing up/creating new account."""

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'placeholder': 'name@example.com',
                'autocomplete': 'username',
            },
        ),
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'placeholder': 'Имя',
                'autocomplete': 'off',
            },
        ),
    )

    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'placeholder': 'Фамилия',
                'autocomplete': 'off',
            },
        ),
    )

    patronymic = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'placeholder': 'Отчество',
                'autocomplete': 'off',
            },
        ),
        required=False,
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'placeholder': 'Пароль',
            },
        ),
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'placeholder': 'Подтверждение пароля',
            },
        ),
    )

    class Meta:
        model = User
        fields = (
            'email',
            'name',
            'surname',
            'patronymic',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = '*Почта'
        self.fields['name'].label = '*Имя'
        self.fields['surname'].label = '*Фамилия'
        self.fields['patronymic'].label = 'Отчество'
        self.fields['password1'].label = '*Пароль'
        self.fields['password2'].label = '*Подтверждение пароля'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _('Пользователь с такой почтой уже существует.'),
            )
        return email


class AuthenticationForm(AuthenticationForm):
    """Custom Authentication form."""

    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'placeholder': 'name@example.com',
                'autocomplete': 'username',
            },
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'placeholder': 'Пароль',
            },
        ),
    )

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Почта'
        self.fields['password'].label = 'Пароль'


class AdminUserChangeForm(UserChangeForm):
    """Form for editing `User` (used on the admin panel)."""

    class Meta:
        model = User
        fields = (
            'email',
            'name',
            'surname',
            'patronymic',
        )


class PasswordResetForm(PasswordResetForm):
    """
    Custom password reset form.

    Send emails using Celery.
    """

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'placeholder': 'name@example.com',
            },
        ),
    )

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Почта'

    def send_mail(
            self,
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None,
    ):
        context['user'] = context['user'].pk
        send_password_reset_code.delay(
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            context=context,
            from_email=from_email,
            to_email=to_email,
            html_email_template_name=html_email_template_name,
        )


class SetPasswordForm(SetPasswordForm):
    """Custom set password form."""

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'placeholder': 'Пароль',
            },
        ),
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'placeholder': 'Подтверждение пароля',
            },
        ),
    )

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password2'].label = 'Подтверждение нового пароля'


class PasswordChangeForm(PasswordChangeForm):
    """Password change form."""

    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'placeholder': 'Старый пароль',
            },
        ),
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'placeholder': 'Новый пароль',
            },
        ),
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'placeholder': 'Подтверждение нового пароля',
            },
        ),
    )

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Старый пароль'
        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password2'].label = 'Подтверждение нового пароля'


class UserInfoForm(forms.ModelForm):
    """Form for editing user info."""

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
                'autocomplete': 'email',
            },
        ),
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
            },
        ),
    )

    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
            },
        ),
    )

    patronymic = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
            },
        ),
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'email',
            'name',
            'surname',
            'patronymic',
        )

    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = '*Почта'
        self.fields['name'].label = '*Имя'
        self.fields['surname'].label = '*Фамилия'
        self.fields['patronymic'].label = 'Отчество'


class ProfileForm(forms.ModelForm):
    """Base form for editing profile info."""

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingField',
            },
        ),
        required=False,
    )
    is_a_student = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'floatingField',
                'style': 'display: block;',
            },
        ),
        required=False,
    )
    from_current_school = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'floatingField',
                'style': 'display: block;',
            },
        ),
        required=False,
    )
    school = forms.ModelChoiceField(
        queryset=School.objects.filter(
            is_current_school=False,
        ),
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'floatingField',
            },
        ),
        required=False,
    )

    class Meta:
        model = Profile
        fields = (
            'date_of_birth',
            'is_a_student',
            'from_current_school',
        )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].label = 'Дата рождения'
        self.fields['is_a_student'].label = 'Являетесь учеником'
        self.fields['is_a_student'].label_attrs = {
            'class': 'form-check-label',
        }
        self.fields['from_current_school'].label = 'Из текущей школы'
        self.fields['from_current_school'].label_attrs = {
            'class': 'form-check-label',
        }
        self.fields['school'].label = 'Школа'


class TeacherProfileForm(ProfileForm):
    """Form for editing teacher info."""

    class Meta(ProfileForm.Meta):
        model = Profile
        fields = (
            'date_of_birth',
            'is_a_student',
            'from_current_school',
            'school',
        )

    def __init__(self, *args, **kwargs):
        exclude_school = kwargs.pop('exclude_school', False)
        super(TeacherProfileForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].label = 'Дата рождения'
        self.fields['is_a_student'].label = 'Являетесь учеником'
        self.fields['from_current_school'].label = 'Из текущей школы'
        self.fields['school'].label = 'Школа'

        if exclude_school:
            del self.fields['school']


class StudentProfileForm(ProfileForm):
    """Form for editing student info."""

    YEAR_CHOICES = [
        (1, '1-й класс'),
        (2, '2-й класс'),
        (3, '3-й класс'),
        (4, '4-й класс'),
        (5, '5-й класс'),
        (6, '6-й класс'),
        (7, '7-й класс'),
        (8, '8-й класс'),
        (9, '9-й класс'),
        (10, '10-й класс'),
        (11, '11-й класс'),
    ]

    year_of_study = forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'floatingField',
                'style': 'display: block;',
            },
        ),
        required=False,
    )

    school_class = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'floatingField',
            },
        ),
        required=False,
    )

    class Meta(ProfileForm.Meta):
        model = Profile
        fields = (
            'date_of_birth',
            'is_a_student',
            'from_current_school',
            'year_of_study',
            'school_class',
            'school',
        )

    def __init__(self, *args, **kwargs):
        exclude_year_of_study = kwargs.pop('exclude_year_of_study', False)
        exclude_school_class = kwargs.pop('exclude_school_class', False)
        exclude_school = kwargs.pop('exclude_school', False)
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].label = 'Дата рождения'
        self.fields['is_a_student'].label = 'Являетесь учеником'
        self.fields['from_current_school'].label = 'Из текущей школы'
        self.fields['year_of_study'].label = 'Класс'
        self.fields['school_class'].label = 'Класс'
        self.fields['school'].label = 'Школа'

        if exclude_year_of_study:
            del self.fields['year_of_study']
        if exclude_school_class:
            del self.fields['school_class']
        if exclude_school:
            del self.fields['school']

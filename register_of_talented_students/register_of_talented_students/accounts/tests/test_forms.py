from django.test import SimpleTestCase

from accounts.forms import SignupForm, SigninForm


class TestSignupForm(SimpleTestCase):
    def test_signup_form_valid_data(self):
        form = SignupForm(
            data={
                'email': 'user@gmail.com',
                'name': 'Name',
                'surname': 'Surname',
                'patronymic': 'Patronymic',
                'password': 'password',
                'confirm_password': 'password',
            }
        )

        self.assertTrue(form.is_valid())

    def test_signup_form_no_data(self):
        form = SignupForm(data={})

        self.assertFalse(form.is_valid())


class TestSigninForm(SimpleTestCase):
    def test_signin_form_valid_data(self):
        form = SigninForm(
            data={
                'email': 'user@gmail.com',
                'password': 'password',
            }
        )

        self.assertTrue(form.is_valid())

    def test_signin_form_no_data(self):
        form = SigninForm(data={})

        self.assertFalse(form.is_valid())

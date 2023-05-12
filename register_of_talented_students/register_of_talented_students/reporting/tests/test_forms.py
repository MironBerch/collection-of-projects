from django.test import SimpleTestCase

from reporting.forms import ContestForm, ContestUpdateForm


class TestContestForm(SimpleTestCase):
    """Base test contest form"""
    def test_contest_form_valid_data(self):
        form = ContestForm(
            data={
                'title': 'contest title',
                'stage': 'Школьный',
                'student': 'Name Surname',
                'subject': 'Информатика',
                'result': 'Призёр',
                'event_date': '2024-12-01',
                'direction': 'Олимпиада',
            }
        )

        self.assertTrue(form.is_valid())

    def test_contest_form_no_data(self):
        form = ContestForm(data={})

        self.assertFalse(form.is_valid())


class TestContestUpdateForm(SimpleTestCase):
    """Base test contest update form"""
    def test_contest_update_form_valid_data(self):
        form = ContestUpdateForm(
            data={
                'title': 'contest title',
                'stage': 'Школьный',
                'student': 'Name Surname',
                'subject': 'Информатика',
                'result': 'Призёр',
                'event_date': '2024-12-01',
                'direction': 'Олимпиада',
            }
        )

        self.assertTrue(form.is_valid())

    def test_contest_update_form_no_data(self):
        form = ContestForm(data={})

        self.assertFalse(form.is_valid())

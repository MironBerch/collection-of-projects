from django.test import TestCase

from accounts.models import User
from reporting.models import Contest
from students.models import Student
from school_classes.models import Class


class TestContestModels(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email='user@gmail.com',
            name='Name',
            surname='Surname',
            password='password',
        )

        self.school_class = Class.objects.create(
            school_class='9в',
        )

        self.student = Student.objects.create(
            full_name='Name Surname Patronymic',
            school_class=self.school_class,
            is_learns=True,
        )

        self.contest = Contest.objects.create(
            contest_creater=self.user,
            title='contest title',
            stage='Школьный',
            student=self.student,
            subject='Информатика',
            result='Призёр',
            event_date='2024-12-01',
            direction='Олимпиада',
        )

    def test_contest_fields(self):
        """Test contest fields"""
        self.assertAlmostEquals(self.contest.contest_creater, self.user)
        self.assertAlmostEquals(self.contest.title, 'contest title')
        self.assertAlmostEquals(self.contest.stage, 'Школьный')
        self.assertAlmostEquals(self.contest.student, self.student)
        self.assertAlmostEquals(self.contest.subject, 'Информатика')
        self.assertAlmostEquals(self.contest.result, 'Призёр')
        self.assertAlmostEquals(self.contest.event_date, '2024-12-01')
        self.assertAlmostEquals(self.contest.direction, 'Олимпиада')

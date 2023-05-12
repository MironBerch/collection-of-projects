from django.test import TestCase

from students.models import Student
from school_classes.models import Class


class TestStudentsModels(TestCase):

    def setUp(self) -> None:
        self.school_class = Class.objects.create(
            school_class='9в',
        )

        self.student = Student.objects.create(
            full_name='Берчетов Мирон Андреевич',
            school_class=self.school_class,
            is_learns=True,
        )

    def test_school_class_fields(self):
        self.assertAlmostEquals(str(self.school_class), '9в')

    def test_student_fields(self):
        """Test student fields"""
        self.assertAlmostEquals(
            self.student.full_name, 'Берчетов Мирон Андреевич'
        )
        self.assertAlmostEquals(str(self.student.school_class), '9в')
        self.assertAlmostEquals(self.student.is_learns, True)

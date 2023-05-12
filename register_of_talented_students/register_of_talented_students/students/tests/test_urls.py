from django.urls import resolve, reverse
from django.test import SimpleTestCase

from students.views import ImportStudentsView, StudentDetailView


class TestStudentUrls(SimpleTestCase):

    def test_import_students_view_is_resolved(self):
        url = reverse('import_students')
        self.assertEquals(
            resolve(url).func.view_class, ImportStudentsView,
        )

    def test_student_detail_view_is_resolved(self):
        url = reverse('student_view', args=[1, ])
        self.assertEquals(
            resolve(url).func.view_class, StudentDetailView,
        )

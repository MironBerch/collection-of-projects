from django.urls import resolve, reverse
from django.test import SimpleTestCase

from school_classes.views import (
    SchoolClassesListView,
    SchoolClassStudentsListView,
)


class TestSchoolClassesUrls(SimpleTestCase):

    def test_school_classes_list_view_is_resolved(self):
        url = reverse('school_classes')
        self.assertEquals(
            resolve(url).func.view_class, SchoolClassesListView,
        )

    def test_school_class_students_list_view_is_resolved(self):
        url = reverse('school_classes_students', args=['1а', ])
        self.assertEquals(
            resolve(url).func.view_class, SchoolClassStudentsListView,
        )

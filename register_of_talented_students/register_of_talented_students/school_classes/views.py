from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin

from school_classes.services import (
    get_all_classes,
    get_number_of_school_classes_students,
)
from students.services import get_students_by_class


class SchoolClassesListView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """View for school classes list"""

    template_name = 'school_classes/school_classes_list.html'

    def get(self, request):
        return self.render_to_response(
            context={
                'school_classes': get_all_classes(),
                'numbers_of_school_classes': get_number_of_school_classes_students(),
            },
        )


class SchoolClassStudentsListView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """View for school class students list"""

    template_name = 'school_classes/school_class_students_list.html'

    def get(self, request, pk):
        return self.render_to_response(
            context={
                'students': get_students_by_class(school_class=pk),
                'school_class': pk,
            },
        )

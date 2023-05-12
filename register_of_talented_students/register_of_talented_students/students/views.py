import os
from django.views import View
from django.http import FileResponse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin

from accounts.mixins import SuperUserRequiredMixin
from students.forms import StudentsImportForm
from students.input import import_students, create_import_students_example
from students.services import (
    get_student_contest_by_id,
    get_student_by_id,
    get_former_students,
)


class ImportStudentsView(
    SuperUserRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """View for import students"""

    template_name = 'students/import_student.html'
    form_class = StudentsImportForm

    def get(self, request):
        return self.render_to_response(
            context={
                'form': self.form_class(),
            },
        )

    def post(self, request):
        form = StudentsImportForm(
            request.POST or None,
            files=request.FILES or None,
        )

        if form.is_valid():
            students = form.save()
            filename = students.file.open('r')
            BASE_DIR = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)),
            )
            filepath = BASE_DIR + '/media/' + str(filename)
            import_students(filepath)
            return redirect('list')

        return self.render_to_response(
            context={
                'form': self.form_class(),
            },
        )


class StudentDetailView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """View for detail student"""

    template_name = 'students/detail_student.html'

    def get(self, request, id):
        return self.render_to_response(
            context={
                'contests': get_student_contest_by_id(id=id),
                'student': get_student_by_id(id=id)
            },
        )


class FormerStudentListView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """View for former students list"""

    template_name = 'students/former_student.html'

    def get(self, request):
        return self.render_to_response(
            context={
                'students': get_former_students()
            },
        )


def download_students_import_example(request):
    """Download example excel file"""
    create_import_students_example()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'students_import_example.xlsx'
    filepath = BASE_DIR + '/media/' + filename
    file = open(filepath, 'rb')
    response = FileResponse(file)
    return response

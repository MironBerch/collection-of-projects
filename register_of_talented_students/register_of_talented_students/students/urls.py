from django.urls import path

from students.views import (
    ImportStudentsView,
    StudentDetailView,
    FormerStudentListView,
    download_students_import_example,
)


urlpatterns = [
    path(
        route='students/import_students/',
        view=ImportStudentsView.as_view(),
        name='import_students',
    ),
    path(
        route='students/<int:id>/',
        view=StudentDetailView.as_view(),
        name='student_view',
    ),
    path(
        route='students/former/',
        view=FormerStudentListView.as_view(),
        name='former_student_view',
    ),
    path(
        route='students/import_students/download_file_example/',
        view=download_students_import_example,
        name='download_students_import_example',
    ),
]

from django.urls import path

from school_classes.views import (
    SchoolClassesListView,
    SchoolClassStudentsListView,
)

urlpatterns = [
    path(
        route='school_classes/',
        view=SchoolClassesListView.as_view(),
        name='school_classes',
    ),
    path(
        route='school_classes/<str:pk>/',
        view=SchoolClassStudentsListView.as_view(),
        name='school_classes_students',
    ),
]

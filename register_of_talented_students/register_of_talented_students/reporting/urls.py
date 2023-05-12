from django.urls import path

from reporting.views import (
    ContestCreateView,
    ContestListView,
    ContestUpdateView,
    ContestDeleteView,
    ContestDetailView,
    ContestExportView,
    render_students_select,
)


urlpatterns = [
    path(
        route='',
        view=ContestListView.as_view(),
        name='list',
    ),
    path(
        route='create/',
        view=ContestCreateView.as_view(),
        name='create',
    ),
    path(
        route='export/',
        view=ContestExportView.as_view(),
        name='export',
    ),
    path(
        route='update/<int:id>/',
        view=ContestUpdateView.as_view(),
        name='update',
    ),
    path(
        route='delete/<int:id>/',
        view=ContestDeleteView.as_view(),
        name='delete',
    ),
    path(
        route='detail/<int:id>/',
        view=ContestDetailView.as_view(),
        name='detail',
    ),

    path(
        route='render_students_select/',
        view=render_students_select,
        name='render_students_select',
    ),
]

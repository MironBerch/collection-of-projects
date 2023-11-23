from django.urls import path

from competitions.views import CompetitionDetailView, CompetitionsListView

urlpatterns = [
    path(
        route='competitions/',
        view=CompetitionsListView.as_view(),
        name='competitions_list',
    ),
    path(
        route='competitions/<int:id>/',
        view=CompetitionDetailView.as_view(),
        name='competition_detail',
    ),
]

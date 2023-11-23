from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin

from competitions.forms import CompetitionFilter
from competitions.services import get_all_competitions, get_competition_by_id


class CompetitionsListView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """View list of competitions."""

    template_name = 'competitions/competitions_list.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.render_to_response(
            context={
                'competitions': CompetitionFilter(
                    data=request.GET,
                    queryset=get_all_competitions(),
                ),
            },
        )


class CompetitionDetailView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """Detail competition view."""

    template_name = 'competitions/competition_detail.html'

    def get(self, request, id):
        return self.render_to_response(
            context={
                'competition': get_competition_by_id(id=id),
            },
        )

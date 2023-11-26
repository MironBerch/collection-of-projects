from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin

from events.forms import EventsFilter, RegistrationForEventForm
from events.services import get_event_by_slug, get_published_events, get_user_awards_with_results


class EventListView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """View list of events."""

    template_name = 'events/events_list.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.render_to_response(
            context={
                'events': EventsFilter(
                    data=request.GET,
                    queryset=get_published_events(),
                ),
            },
        )


class EventDetailView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """Detail event view."""

    template_name = 'events/event_detail.html'

    def get(self, request, slug):
        return self.render_to_response(
            context={
                'event': get_event_by_slug(slug=slug),
            },
        )


class RegisterOnEventView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """Detail event view."""

    template_name = 'events/register_on_event.html'

    def get(self, request, slug):
        event = get_event_by_slug(slug=slug)
        return self.render_to_response(
            context={
                'form': RegistrationForEventForm(event=event),
                'event': event,
            },
        )


class AwardListView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """View list of awards."""

    template_name = 'awards/award_list.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.render_to_response(
            context={
                'awards': get_user_awards_with_results(user=request.user),
            },
        )

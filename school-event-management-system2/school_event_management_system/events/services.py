from django.db.models import Prefetch, QuerySet
from django.shortcuts import get_object_or_404

from accounts.models import User
from events.models import Award, Event, Result


def get_all_events() -> QuerySet[Event]:
    """Return all `Event`'s."""
    return Event.objects.all()


def get_published_events() -> QuerySet[Event]:
    """Return all published `Event`'s."""
    return Event.objects.filter(published=True)


def get_event_by_slug(slug: int) -> Event:
    """Return `Event` by id."""
    return get_object_or_404(Event, slug=slug)


def get_user_awards_with_results(user: User) -> QuerySet[Award]:
    """Return user's Awards with associated Results."""
    return Award.objects.filter(
        participant__user=user,
    ).select_related(
        'event',
    ).prefetch_related(
        Prefetch(
            'event__results',
            queryset=Result.objects.filter(
                participant__user=user,
            ),
        ),
    )

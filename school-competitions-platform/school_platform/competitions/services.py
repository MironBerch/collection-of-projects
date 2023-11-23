from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from competitions.models import Competition


def get_all_competitions() -> QuerySet[Competition]:
    """Return all `Competition`'s."""
    return Competition.objects.all()


def get_competition_by_id(id: int) -> Competition:
    """Return `Competition` by id."""
    return get_object_or_404(Competition, id=id)

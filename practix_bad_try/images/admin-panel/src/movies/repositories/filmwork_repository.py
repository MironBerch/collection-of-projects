from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F, Q, QuerySet

from movies.enums import PersonRole
from movies.models import Filmwork


class FilmworkRepository:
    """Абстракция для работы с данными фильмов."""

    @staticmethod
    def get_filmworks_with_related_data() -> QuerySet[Filmwork]:
        filmworks_data = (
            Filmwork.objects
            .annotate(
                genres_list=ArrayAgg(
                    'genres__name',
                    distinct=True,
                ),
                actors_list=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role=PersonRole.ACTOR.value),
                    distinct=True,
                ),
                directors_list=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role=PersonRole.DIRECTOR.value),
                    distinct=True,
                ),
                writers_list=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role=PersonRole.WRITER.value),
                    distinct=True,
                ),
            )
            .values(
                'id',
                'title',
                'description',
                'release_date',
                'rating',
                'type',
                'age_rating',
                'access_type',
            )
            .annotate(
                genres=F('genres_list'),
                actors=F('actors_list'),
                directors=F('directors_list'),
                writers=F('writers_list'),
            )
        )
        return filmworks_data

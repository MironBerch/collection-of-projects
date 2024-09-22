from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from movies.models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 0


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    extra = 0


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'get_roles')
    list_filter = ('personfilmwork__role', )
    search_fields = ('full_name', 'id')

    @admin.display(description='роль')
    def get_roles(self, object: Person) -> str:
        """Вывод ролей участников кинопроизведений."""
        return ', '.join(
            [str(personfilmwork.role) for personfilmwork in object.personfilmwork_set.all()],
        )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created',
        'rating',
        'get_genres',
        'get_persons',
    )
    list_filter = ('type', 'genres')
    search_fields = (
        'id',
        'title',
        'description',
        'persons__full_name',
    )
    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Filmwork]:
        """Загрузка кинопроизведений и связанных данных."""
        queryset = super().get_queryset(request)
        if request.resolver_match.view_name.endswith('change'):
            return queryset.prefetch_related('genres', 'persons')
        return queryset

    @admin.display(description='жанры')
    def get_genres(self, object: Filmwork) -> str:
        """Вывод жанров кинопроизведения."""
        return ', '.join([genre.name for genre in object.genres.all()])

    @admin.display(description='участники')
    def get_persons(self, object: Filmwork) -> str:
        """Вывод имён персонала съемочной группы кинопроизведения."""
        return ', '.join([person.full_name for person in object.persons.all()])

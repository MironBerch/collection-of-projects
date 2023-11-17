from django.contrib import admin

from movies.models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 0


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    extra = 0


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'created',
    )
    search_fields = ('name', )


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'type',
        'rating',
        'release_date',
    )
    search_fields = ('title', )
    list_filter = (
        'type',
        'access_type',
    )
    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.resolver_match.view_name.endswith('change'):
            return queryset.prefetch_related('genres', 'persons')
        return queryset


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', )
    search_fields = ('full_name', )

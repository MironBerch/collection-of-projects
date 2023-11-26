from django.contrib import admin

from events.models import Award, Event, Participant, RegistrationForEventField, Result, Team


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name', ),
    }
    list_display = (
        'name',
        'slug',
        'status',
        'type',
        'date_of_starting_event',
        'published',
    )
    search_fields = (
        'name',
        'slug',
    )
    list_filter = (
        'status',
        'type',
        'published',
    )
    ordering = (
        'status',
        'type',
        'published',
    )

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'slug',
                    'image',
                    'description',
                    'type',
                    'status',
                ),
            },
        ),
        (
            'Количество участников', {
                'fields': (
                    'maximum_number_of_event_participants',
                    'maximum_commands',
                    'maximum_commands_per_class',
                    'maximum_number_of_team_members',
                    'minimum_number_of_team_members',
                ),
            },
        ),
        (
            'Настройки видимости конкурса', {
                'fields': (
                    'published',
                ),
            },
        ),
        (
            'Даты',
            {
                'fields': (
                    'date_of_ending_registration',
                    'date_of_starting_registration',
                    'date_of_starting_event',
                ),
            },
        ),
    )


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'event',
        'user',
        'team',
    )
    search_fields = (
        'event__name',
        'user',
        'team__name',
    )
    list_filter = (
        'event',
        'team',
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'event',
        'name',
    )
    search_fields = (
        'event__name',
        'name',
    )
    list_filter = ('event', )


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = (
        'event',
        'participant',
        'diplom',
    )
    search_fields = (
        'event__name',
        'participant__user',
    )
    list_filter = ('event', )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'event',
        'participant',
        'team',
        'result',
    )
    search_fields = (
        'event__name',
        'participant__user',
        'team__name',
    )
    list_filter = ('event', )


@admin.register(RegistrationForEventField)
class RegistrationForEventFieldAdmin(admin.ModelAdmin):
    list_display = (
        'event',
        'label',
        'field_type',
        'is_blank',
    )
    search_fields = (
        'event',
    )
    list_filter = (
        'event',
        'field_type',
        'is_blank',
    )

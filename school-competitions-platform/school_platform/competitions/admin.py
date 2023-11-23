from django.contrib import admin

from competitions.models import Competition, Participant, Reward, Team


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_competition_individual',
        'status',
        'only_for_current_school',
        'is_draft',
    )
    search_fields = ('name', )
    readonly_fields = ('id', )
    ordering = ('id', )

    list_filter = (
        'status',
        'is_competition_individual',
        'only_for_current_school',
        'is_draft',
    )

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'image',
                    'description',
                ),
            },
        ),
        (
            'Количество участников', {
                'fields': (
                    'maximum_number_of_event_participants',
                    'maximum_commands',
                    'maximum_number_of_team_members',
                    'maximum_commands_per_class',
                ),
            },
        ),
        (
            'Условия конкурса', {
                'fields': (
                    'only_for_current_school',
                    'commands_only_from_classes',
                    'is_competition_individual',
                    'status',
                    'is_draft',
                ),
            },
        ),
        (
            'Даты',
            {
                'fields': (
                    'date_of_ending_registration',
                    'date_of_starting_registration',
                    'date_of_starting_competition',
                ),
            },
        ),
        (
            'Списки участвующих',
            {
                'fields': (
                    'participants',
                    'teams',
                ),
            },
        ),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'school_class',
        'competition',
    )
    search_fields = (
        'name',
        'school_class',
    )
    readonly_fields = ('id', )
    ordering = ('id', )


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'competition',
        'participant',
    )
    search_fields = (
        'competition',
        'participant',
    )
    readonly_fields = ('id', )
    ordering = ('id', )


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = (
        'participant',
        'competition',
    )
    search_fields = (
        'participant',
        'competition',
    )
    readonly_fields = ('id', )
    ordering = ('id', )

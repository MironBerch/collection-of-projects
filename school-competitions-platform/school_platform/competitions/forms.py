import django_filters

from django import forms

from competitions.models import Competition


class CompetitionFilter(django_filters.FilterSet):
    """Form for filter transaction queryset."""

    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Поиск по названию',
            },
        ),
    )

    def __init__(self, *args, **kwargs):
        super(CompetitionFilter, self).__init__(*args, **kwargs)
        self.filters['name'].label = 'Поиск по названию'

    class Meta:
        model = Competition
        fields = (
            'name',
            'status',
            'only_for_current_school',
            'is_competition_individual',
        )

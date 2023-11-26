import django_filters

from django import forms

from events.models import Event, RegistrationForEventField


class EventsFilter(django_filters.FilterSet):
    """Form for filter event queryset."""

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
        super(EventsFilter, self).__init__(*args, **kwargs)
        self.filters['name'].label = 'Поиск по названию'

    class Meta:
        model = Event
        fields = (
            'name',
            'status',
            'type',
        )


class RegistrationForEventForm(forms.Form):
    def __init__(self, event, *args, **kwargs):
        super(RegistrationForEventForm, self).__init__(*args, **kwargs)
        registration_fields = RegistrationForEventField.objects.filter(
            event=event,
        )
        for field in registration_fields:
            self.fields[field.label] = field.create_form_field()

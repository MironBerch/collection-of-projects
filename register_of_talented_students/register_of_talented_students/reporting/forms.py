from django import forms

from reporting.models import Contest


class ContestForm(forms.ModelForm):
    event_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        ),
    )

    class Meta:
        model = Contest
        fields = (
            'event_date',
            'title',
            'other',
            'teachers_name',
            'stage',
            'direction',
            'subject',
            'result',
            'scan_diploma',
        )
        widgets = {
            'scan_diploma': forms.FileInput(
                attrs={
                    'id': 'formFile',
                    'type': 'file',
                }
            ),
        }


class ContestUpdateForm(ContestForm):
    event_date = forms.DateField(
        widget=forms.DateInput(),
    )

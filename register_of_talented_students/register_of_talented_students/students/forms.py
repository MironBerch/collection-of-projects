from django import forms

from students.models import StudentsBase


class StudentsImportForm(forms.ModelForm):

    class Meta:
        model = StudentsBase
        fields = ('file',)

import os
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.views import View
from django.views.generic.base import TemplateResponseMixin

from reporting.forms import ContestForm, ContestUpdateForm
from reporting.services import (
    get_all_contests, get_users_creation_contests, get_contest,
)
from reporting.export import export_contest_to_excel
from students.services import get_students_by_class, get_student_by_full_name
from school_classes.services import get_all_classes


class ContestCreateView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View
):
    """View for create contest"""

    template_name = 'reporting/create_report.html'
    form_class = ContestForm

    def get(self, request):
        return self.render_to_response(
            context={
                'form': self.form_class(),
                'classes': get_all_classes(),
            },
        )

    def post(self, request):
        form = ContestForm(request.POST or None, files=request.FILES or None)

        if form.is_valid():
            contest = form.save(commit=False)
            contest.student = get_student_by_full_name(
                request.POST.get('reporting_student'),
            )
            contest.contest_creater = request.user
            contest.save()
            return redirect('list')

        return self.render_to_response(
            context={
                'form': form,
                'classes': get_all_classes(),
            },
        )


class ContestListView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """View for contest list"""

    template_name = 'reporting/report_list.html'

    def get(self, request):
        if request.user.is_superuser:
            contests = get_all_contests()
        else:
            contests = get_users_creation_contests(user=request.user)

        return self.render_to_response(
            context={
                'contests': contests,
            },
        )


class ContestUpdateView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """View for contest update"""

    template_name = 'reporting/update_report.html'

    def get(self, request, id):
        contest = get_contest(id=id)

        if not (
            request.user.is_superuser or
            request.user == contest.contest_creater
        ):
            return redirect('list')

        form = ContestUpdateForm(
            request.POST or None,
            instance=contest,
            files=request.FILES or None,
        )

        return self.render_to_response(
            context={
                'form': form,
                'contest': contest,
                'classes': get_all_classes(),
            },
        )

    def post(self, request, id):
        contest = get_contest(id=id)
        form = ContestUpdateForm(
            request.POST or None,
            instance=contest,
            files=request.FILES or None,
        )

        if form.is_valid():
            contest = form.save()
            contest.student = get_student_by_full_name(
                request.POST['reporting_student'],
            )
            contest.save()
            return redirect('detail', id=id)

        return redirect('update', id=id)


class ContestDeleteView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """View for delete contest"""

    template_name = 'reporting/delete_report.html'

    def get(self, request, id):
        contest = get_contest(id=id)

        if not (
            request.user.is_superuser or 
            request.user == contest.contest_creater
        ):
            return redirect('list')

        return self.render_to_response(
            context={
                'contest': contest,
            },
        )

    def post(self, request, id):
        contest = get_contest(id=id)
        contest.delete()
        return redirect('list')


class ContestDetailView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """View for detail contest"""

    template_name = 'reporting/detail_report.html'

    def get(self, request, id):
        contest = get_contest(id=id)

        return self.render_to_response(
            context={
                'contest': contest,
            },
        )


class ContestExportView(LoginRequiredMixin, View):
    """View for export contest"""

    def get(self, request):
        return render(request, 'reporting/export_report.html')

    def post(self, request):
        if request.user.is_superuser:
            contests = get_all_contests()
        else:
            contests = get_users_creation_contests(user=request.user)

        export_contest_to_excel(contests)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = 'export.xlsx'
        filepath = BASE_DIR + '/media/' + filename
        file = open(filepath, 'rb')
        response = FileResponse(file)
        return response


def render_students_select(request):
    """render students select by using htmx"""
    school_class = request.GET.get('school_class')
    context = {
        'students': get_students_by_class(school_class),
    }
    return render(request, 'includes/students_select.html', context)

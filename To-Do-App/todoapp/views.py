from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from .models import Task


class LoginView(LoginView):
    """User login page"""
    template_name = 'todoapp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterPage(FormView):
    """User register page"""
    template_name = 'todoapp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    """Task list page"""
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    """Task create page"""
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('home')
    template_name = 'todoapp/task_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    """Detail task page and update task page"""
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('home')


class TaskDelete(LoginRequiredMixin, DeleteView):
    """Delete task page"""
    model = Task
    success_url = reverse_lazy('home')
    template_name = 'todoapp/task_confirm_delete.html'
    context_object_name = 'home'
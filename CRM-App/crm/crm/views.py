import random
from django.core.mail import send_mail
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from .mixins import OrganisorAndLoginRequiredMixin
import logging
import datetime
from django import contrib
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from crm.mixins import OrganisorAndLoginRequiredMixin
from crm.models import Lead, Agent, Category, FollowUp, Agent
from crm.forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm, CategoryModelForm, FollowUpModelForm, AgentModelForm
from django.views import View


class AgentListView(View, OrganisorAndLoginRequiredMixin):
    def get(self, request):
        organisation = self.request.user.userprofile
        object_list = Agent.objects.filter(organisation=organisation)
        context = {
            'object_list': object_list,
        }
        return render(request, 'agents/agent_list.html', context)


class AgentCreateView(View, OrganisorAndLoginRequiredMixin):
    def get(self, request):
        form = AgentModelForm()
        context = {
            'form': form,
        }
        return render(request, 'agents/agent_create.html', context)
    
    def post(self, request):
        form = AgentModelForm(request.POST)
        #if form.is
        #context = {
        #    'form': form,
        #}
        #return render(request, 'agents/agent_create.html', context)
        #'email', 'username', 'first_name', 'last_name'
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = form.save(commit=False)
            user.is_agent = True
            user.is_orgaisor = False
            user.set_password(f'{random.randint(0, 1000000)}')
            user.save()
            Agent.objects.create(user=user, organisation=self.request.user.userprofile)
            return redirect('agent-list')
        return redirect('agent-create')


class AgentListView(View, OrganisorAndLoginRequiredMixin):
    def get(self, request):
        organisation = self.request.user.userprofile
        agent = Agent.objects.filter(organisation=organisation)
        context = {
            'agent': agent,
        }
        return render(request, 'agents/agent_detail.html', context)


class AgentListView(View, OrganisorAndLoginRequiredMixin):
    def get(self, request):
        form = AgentModelForm(request.POST)
        context = {
            'form': form,
        }
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = form.save(commit=False)
            user.is_agent = True
            user.is_orgaisor = False
            user.set_password(f'{random.randint(0, 1000000)}')
            user.save()
            Agent.objects.create(user=user, organisation=self.request.user.userprofile)
            return redirect('agent-list')
        return redirect('agent-create')

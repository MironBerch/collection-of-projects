from django.views import View
from django.shortcuts import redirect
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from profiles.forms import ProfileForm, ProfileCommentForm
from accounts.services import get_user_by_username
from profiles.services import get_user_profile, get_profile_comments, create_profile_comment


class ProfileEdit(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """Profile edit view"""

    form_class = ProfileForm
    template_name = 'profiles/profile_edit.html'

    def get(self, request, username):
        user = get_user_by_username(username=username)
        profile = get_user_profile(user=user)
        return self.render_to_response(
            context={
                'form': self.form_class(instance=profile),
            },
        )

    def post(self, request, username):
        user = get_user_by_username(username=username)
        profile = get_user_profile(user=user)
        form = ProfileForm(request.POST or None, instance=profile, files=request.FILES or None)

        if form.is_valid():
            form.save()
            return redirect('signout')
        
        return self.render_to_response(
            context={
                'form': self.form_class(instance=profile),
            },
        )
    

class ProfileView(
    TemplateResponseMixin,
    View,
):
    form_class = ProfileCommentForm
    template_name = 'profiles/profile_view.html'

    def get(self, request, username):
        user = get_user_by_username(username=username)
        profile = get_user_profile(user=user)
        comments = get_profile_comments(profile)
        return self.render_to_response(
            context={
                'user': user,
                'profile': profile,
                'comments': comments,
                'form': self.form_class(),
            },
        )
    
    def post(self, request, username):
        user = get_user_by_username(username=username)
        profile = get_user_profile(user=user)
        comments = get_profile_comments(profile=profile)
        form = ProfileCommentForm(request.POST or None)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            create_profile_comment(profile=profile, author=request.user, content=content)
            return redirect('profile_view', username=username)
        
        return self.render_to_response(
            context={
                'user': user,
                'profile': profile,
                'comments': comments,
                'form': self.form_class(),
            },
        )
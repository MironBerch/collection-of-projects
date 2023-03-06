from django.shortcuts import redirect


class AnonymousUserRequiredMixin:
    """Verify that user is not logged in"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('signout')
        return super(AnonymousUserRequiredMixin, self).dispatch(request, *args, **kwargs)


class EmailNotConfirmedUserRequiredMixin:
    """Verify that user has not email confirmed"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_email_confirmed:
            return redirect('signout')
        return super(EmailNotConfirmedUserRequiredMixin, self).dispatch(request, *args, **kwargs)
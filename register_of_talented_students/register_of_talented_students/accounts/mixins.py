from django.shortcuts import redirect


class SuperUserRequiredMixin:
    """Verify that user is superuser"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('list')
        return super(
            SuperUserRequiredMixin, self
        ).dispatch(request, *args, **kwargs)


class AnonymousUserRequiredMixin:
    """Verify that user is not logged in"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('signout')
        return super(
            AnonymousUserRequiredMixin, self
        ).dispatch(request, *args, **kwargs)

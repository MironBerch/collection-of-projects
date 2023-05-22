from django.shortcuts import redirect


class AnonymousUserRequiredMixin:
    """
    Verify that user is not logged in.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('signout')
        return super(AnonymousUserRequiredMixin, self,).dispatch(request, *args, **kwargs)

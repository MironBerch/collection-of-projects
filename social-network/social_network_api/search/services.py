from accounts.models import User


def get_search_queryset():
    return (
        User.objects.select_related('profile')
        .prefetch_related('following')
        .prefetch_related('followers')
    )

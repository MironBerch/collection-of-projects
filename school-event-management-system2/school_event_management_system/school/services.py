from django.shortcuts import get_object_or_404

from accounts.models import User
from school.models import Class


def get_school_class(school_class: str) -> Class:
    """Get school class."""
    return get_object_or_404(Class, school_class=school_class)


def set_new_class_teacher_for_school_class(user: User, school_class: str) -> None:
    """Set new class teacher for school class."""
    if school_class:
        user.profile.school_class = get_school_class(school_class)
        user.profile.save()
        school_class = get_school_class(school_class)
        school_class.class_teacher = user
        school_class.save()
    else:
        user.profile.school_class = None
        user.profile.save()
        school_class.class_teacher = None
        school_class.save()

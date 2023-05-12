from django.shortcuts import get_object_or_404

from school_classes.models import Class
from students.models import Student


def get_school_class(school_class: str):
    """Get school class model by school class name"""
    student_class = get_object_or_404(
        Class,
        school_class=school_class,
    )
    return student_class


def get_all_classes():
    """Get all classes"""
    classes_list = []
    ordered_school_classes = []

    school_classes = Class.objects.all()

    for school_class in school_classes:
        classes_list.append(school_class.school_class)

    classes_list.sort(key=lambda x: (int(x[:-1]), x[-1]))

    for school_class in classes_list:
        school_class = Class.objects.get(
            school_class=school_class,
        )
        ordered_school_classes.append(school_class)

    return ordered_school_classes


def create_school_class_if_not_exist(school_class: str) -> None:
    """Create school class if it not exist in database"""
    if not Class.objects.filter(school_class=school_class).exists():
        Class.objects.create(
            school_class=school_class,
        )


def get_number_of_school_classes_students():
    """Count learning school class students"""
    number_of_school_classes_students_list = []
    school_classes = get_all_classes()
    for school_class in school_classes:
        number_of_school_classes_students_list.append(
            Student.objects.filter(
                school_class=school_class,
                is_learns=True,
            ).count()
        )
    return number_of_school_classes_students_list

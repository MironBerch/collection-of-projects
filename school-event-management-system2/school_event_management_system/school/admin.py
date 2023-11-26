from django.contrib import admin

from school.models import Class


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = (
        'school_class',
        'year_of_study',
        'class_teacher',
    )
    search_fields = (
        'school_class',
        'year_of_study',
        'class_teacher',
    )

    ordering = (
        'school_class',
        'year_of_study',
    )

    fieldsets = (
        (
            'Информация о классе', {
                'fields': (
                    'school_class',
                    'year_of_study',
                    'class_teacher',
                ),
            },
        ),
    )

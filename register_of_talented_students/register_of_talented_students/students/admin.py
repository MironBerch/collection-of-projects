from django.contrib import admin

from students.models import Student, StudentsBase


@admin.register(Student)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'school_class',
        'is_learns',
    )
    list_filter = (
        'school_class',
        'is_learns',
    )
    search_fields = (
        'full_name',
        'school_class',
    )


admin.site.register(StudentsBase)

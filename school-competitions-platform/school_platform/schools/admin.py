from django.contrib import admin

from schools.models import Class, School


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
    list_filter = ('year_of_study', )


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        'school_name',
        'is_current_school',
    )
    search_fields = ('school_name', )
    list_filter = ('is_current_school', )

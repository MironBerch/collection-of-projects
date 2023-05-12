from django.contrib import admin

from school_classes.models import Class


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = (
        'school_class',
    )

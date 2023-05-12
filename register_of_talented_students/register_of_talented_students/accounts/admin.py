from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'name',
        'surname',

        'is_active',
        'is_verified',
        'is_superuser',
    )
    list_filter = (
        'is_active',
        'is_verified',
        'is_superuser',
    )
    search_fields = (
        'email',
        'name',
        'surname',
    )

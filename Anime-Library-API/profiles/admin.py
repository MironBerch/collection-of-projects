from django.contrib import admin

from profiles.models import Profile, ProfileComment


admin.site.register(Profile)
admin.site.register(ProfileComment)
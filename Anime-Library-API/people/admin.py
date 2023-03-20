from django.contrib import admin

from people.models import Person, PersonComment


admin.site.register(Person)
admin.site.register(PersonComment)
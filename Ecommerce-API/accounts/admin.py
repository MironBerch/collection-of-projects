from django.contrib import admin
from django.contrib.auth.models import User

from accounts.models import (
    PhoneNumber,
    Profile,
    Address,
)


admin.site.register(User)
admin.site.register(PhoneNumber)
admin.site.register(Profile)
admin.site.register(Address)

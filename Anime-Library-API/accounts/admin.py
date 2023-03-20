from django.contrib import admin
from accounts.models import User, EmailConfirmMessage


admin.site.register(User)
admin.site.register(EmailConfirmMessage)
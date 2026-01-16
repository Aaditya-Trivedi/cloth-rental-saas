from django.contrib import admin
from .models import LoginAttempt, LoginLog

admin.site.register(LoginAttempt)
admin.site.register(LoginLog)
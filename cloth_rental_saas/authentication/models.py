from django.db import models
from django.contrib.auth.models import User

class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    failed_attempts = models.PositiveIntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    last_attempt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Locked: {self.is_locked}"


class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    login_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[('SUCCESS', 'Success'), ('FAILED', 'Failed')]
    )

    def __str__(self):
        return f"{self.user.username} - {self.status}"

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import LoginAttempt, LoginLog
from notifications.email_service import login_alert


def login_view(request):
    message = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        ip = request.META.get("REMOTE_ADDR")

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            message = "Invalid username or password"
            return render(request, "auth/login.html", {"message": message})

        attempt, _ = LoginAttempt.objects.get_or_create(user=user_obj)

        # 🔒 Account already locked
        if attempt.is_locked:
            LoginLog.objects.create(
                user=user_obj,
                ip_address=ip,
                status="FAILED"
            )
            send_login_alert(user_obj.email, "ACCOUNT LOCKED")
            message = "Account is locked due to multiple failed attempts"
            return render(request, "auth/login.html", {"message": message})

        user = authenticate(request, username=username, password=password)

        # ✅ Successful login
        if user:
            login(request, user)

            attempt.failed_attempts = 0
            attempt.is_locked = False
            attempt.save()

            LoginLog.objects.create(
                user=user,
                ip_address=ip,
                status="SUCCESS"
            )

            login_alert(user.email, "SUCCESSFUL LOGIN")

            return redirect("dashboard")

        # ❌ Failed login
        attempt.failed_attempts += 1
        if attempt.failed_attempts >= 3:
            attempt.is_locked = True

        attempt.save()

        LoginLog.objects.create(
            user=user_obj,
            ip_address=ip,
            status="FAILED"
        )

        if attempt.is_locked:
            login_alert(user_obj.email, "ACCOUNT LOCKED")
            message = "Account locked after 3 failed login attempts"
        else:
            login_alert(user_obj.email, "FAILED LOGIN ATTEMPT")
            message = "Invalid username or password"

    return render(request, "auth/login.html", {"message": message})


def logout_view(request):
    logout(request)
    return render(request, "auth/logout_confirm.html")

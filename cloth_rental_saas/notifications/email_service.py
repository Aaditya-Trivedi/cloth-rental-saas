from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, to_email):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=True,
    )


def login_alert(email, status):
    send_email(
        "Login Alert",
        f"Your account login status: {status}",
        email
    )


def rental_alert(email, cloth_code, return_date):
    send_email(
        "Rental Confirmation",
        f"Cloth {cloth_code} rented successfully. Return by {return_date}.",
        email
    )


def return_alert(email, cloth_code, fine):
    send_email(
        "Return Confirmation",
        f"Cloth {cloth_code} returned. Fine amount: ₹{fine}.",
        email
    )


def overdue_alert(email, cloth_code, fine):
    send_email(
        "Overdue Alert",
        f"Cloth {cloth_code} is overdue. Current fine: ₹{fine}.",
        email
    )
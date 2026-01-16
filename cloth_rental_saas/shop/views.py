from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Sum

from .models import Cloth, Customer, Rental
from notifications.email_service import rental_alert, return_alert, overdue_alert
from notifications.sms_service import send_sms

# NOTE:
# 'shop_1' is used for demo purposes.
# In production, this will be dynamically selected per logged-in shop.

SHOP_DB = "shop_1"
DAILY_FINE = 50


@login_required
def dashboard(request):
    return render(request, "shop/dashboard.html")


@login_required
def rent_cloth(request):
    message = None

    if request.method == "POST":
        cloth_code = request.POST.get("cloth_code")
        name = request.POST.get("customer_name")
        phone = request.POST.get("customer_phone")
        return_date = request.POST.get("return_date")

        try:
            cloth = Cloth.objects.using(SHOP_DB).get(
                cloth_code=cloth_code,
                is_available=True
            )
        except Cloth.DoesNotExist:
            message = "Cloth not available"
            return render(request, "shop/rent.html", {"message": message})

        customer, _ = Customer.objects.using(SHOP_DB).get_or_create(
            name=name,
            phone=phone
        )

        rental = Rental.objects.using(SHOP_DB).create(
            cloth=cloth,
            customer=customer,
            expected_return_date=return_date
        )

        cloth.is_available = False
        cloth.save(using=SHOP_DB)

        # 🔔 Notifications
        rental_alert(
            customer.email or "demo@example.com",
            cloth.cloth_code,
            return_date
        )

        send_sms(
            customer.phone,
            f"Cloth {cloth.cloth_code} rented. Return by {return_date}."
        )

        message = "Cloth rented successfully"

    return render(request, "shop/rent.html", {"message": message})


@login_required
def return_cloth(request):
    message = None

    if request.method == "POST":
        cloth_code = request.POST.get("cloth_code")

        try:
            rental = Rental.objects.using(SHOP_DB).get(
                cloth__cloth_code=cloth_code,
                status="RENTED"
            )
        except Rental.DoesNotExist:
            message = "Active rental not found for this cloth"
            return render(request, "shop/return.html", {"message": message})

        today = date.today()
        rental.actual_return_date = today

        if today > rental.expected_return_date:
            days_late = (today - rental.expected_return_date).days
            rental.fine_amount = days_late * DAILY_FINE
            rental.status = "OVERDUE"
        else:
            rental.fine_amount = 0
            rental.status = "RETURNED"

        rental.save(using=SHOP_DB)

        cloth = rental.cloth
        cloth.is_available = True
        cloth.save(using=SHOP_DB)

        # 🔔 Notifications
        if rental.fine_amount > 0:
            overdue_alert(
                rental.customer.email or "demo@example.com",
                cloth_code,
                rental.fine_amount
            )
        else:
            return_alert(
                rental.customer.email or "demo@example.com",
                cloth_code,
                rental.fine_amount
            )

        send_sms(
            rental.customer.phone,
            f"Return processed. Fine: ₹{rental.fine_amount}"
        )

        message = f"Cloth returned successfully. Fine: ₹{rental.fine_amount}"

    return render(request, "shop/return.html", {"message": message})


@login_required
def inventory_report(request):
    cloths = Cloth.objects.using(SHOP_DB).all()
    return render(request, "shop/reports/inventory.html", {"cloths": cloths})


@login_required
def rented_report(request):
    rentals = Rental.objects.using(SHOP_DB).filter(status="RENTED")
    return render(request, "shop/reports/rented.html", {"rentals": rentals})


@login_required
def overdue_report(request):
    rentals = Rental.objects.using(SHOP_DB).filter(status="OVERDUE")
    return render(request, "shop/reports/overdue.html", {"rentals": rentals})


@login_required
def fine_report(request):
    total_fine = Rental.objects.using(SHOP_DB).aggregate(
        total=Sum("fine_amount")
    )["total"] or 0

    rentals = Rental.objects.using(SHOP_DB).filter(fine_amount__gt=0)

    return render(
        request,
        "shop/reports/fine.html",
        {"rentals": rentals, "total": total_fine},
    )

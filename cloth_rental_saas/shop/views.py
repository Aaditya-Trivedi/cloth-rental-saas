from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Cloth, Customer, Rental
from django.db.models import Sum

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
            cloth = Cloth.objects.using("shop_1").get(cloth_code=cloth_code, is_available=True)
        except Cloth.DoesNotExist:
            message = "Cloth not available"
            return render(request, "shop/rent.html", {"message": message})

        customer, _ = Customer.objects.using("shop_1").get_or_create(
            name=name,
            phone=phone
        )

        Rental.objects.using("shop_1").create(
            cloth=cloth,
            customer=customer,
            expected_return_date=return_date
        )

        cloth.is_available = False
        cloth.save(using="shop_1")

        message = "Cloth rented successfully"

    return render(request, "shop/rent.html", {"message": message})

@login_required
def return_cloth(request):
    message = None

    if request.method == "POST":
        cloth_code = request.POST.get("cloth_code")

        try:
            rental = Rental.objects.using("shop_1").get(
                cloth__cloth_code=cloth_code,
                status="RENTED"
            )
        except Rental.DoesNotExist:
            message = "Active rental not found for this cloth"
            return render(request, "shop/return.html", {"message": message})

        today = date.today()
        rental.actual_return_date = today

        # Fine calculation
        if today > rental.expected_return_date:
            days_late = (today - rental.expected_return_date).days
            rental.fine_amount = days_late * 50
            rental.status = "OVERDUE"
        else:
            rental.fine_amount = 0
            rental.status = "RETURNED"

        rental.save(using="shop_1")

        cloth = rental.cloth
        cloth.is_available = True
        cloth.save(using="shop_1")

        message = f"Cloth returned successfully. Fine: ₹{rental.fine_amount}"

    return render(request, "shop/return.html", {"message": message})

@login_required
def inventory_report(request):
    cloths = Cloth.objects.using("shop_1").all()
    return render(request, "shop/reports/inventory.html", {"cloths": cloths})

@login_required
def rented_report(request):
    rentals = Rental.objects.using("shop_1").filter(status="RENTED")
    return render(request, "shop/reports/rented.html", {"rentals": rentals})

@login_required
def overdue_report(request):
    rentals = Rental.objects.using("shop_1").filter(status="OVERDUE")
    return render(request, "shop/reports/overdue.html", {"rentals": rentals})

@login_required
def fine_report(request):
    total_fine = Rental.objects.using("shop_1").aggregate(
        total=Sum("fine_amount")
    )["total"] or 0

    rentals = Rental.objects.using("shop_1").filter(fine_amount__gt=0)

    return render(
        request,
        "shop/reports/fine.html",
        {"rentals": rentals, "total": total_fine},
    )
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Cloth, Customer, Rental

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
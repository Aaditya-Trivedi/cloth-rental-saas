from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from .models import ShopRegistry, Subscription

def is_superadmin(user):
    return user.is_superuser


@user_passes_test(is_superadmin)
def admin_dashboard(request):
    total_shops = ShopRegistry.objects.count()
    active_shops = ShopRegistry.objects.filter(is_active=True).count()
    revenue = Subscription.objects.aggregate(
        total=Sum("amount_paid")
    )["total"] or 0

    return render(
        request,
        "master/dashboard.html",
        {
            "total_shops": total_shops,
            "active_shops": active_shops,
            "revenue": revenue,
        },
    )


@user_passes_test(is_superadmin)
def shop_list(request):
    shops = ShopRegistry.objects.all()
    return render(request, "master/shop_list.html", {"shops": shops})


@user_passes_test(is_superadmin)
def toggle_shop(request, shop_id):
    shop = ShopRegistry.objects.get(id=shop_id)
    shop.is_active = not shop.is_active
    shop.save()
    return redirect("admin_shops")

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta
from django.utils.crypto import get_random_string

from .models import ShopRegistry, Subscription, SubscriptionPlan
from .utils import create_shop_database


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

@require_POST
@user_passes_test(is_superadmin)
def toggle_shop(request, shop_id):
    shop = ShopRegistry.objects.get(id=shop_id)
    shop.is_active = not shop.is_active
    shop.save()
    return redirect("admin_shops")

@user_passes_test(is_superadmin)
def add_shop(request):
    plans = SubscriptionPlan.objects.all()
    message = None
    error = None

    if request.method == "POST":
        try:
            shop_name = request.POST.get("shop_name")
            owner_name = request.POST.get("owner_name")
            email = request.POST.get("email")
            plan_id = request.POST.get("plan")

            # ✅ 1. CREATE SAFE, MEANINGFUL DB NAME
            shop_slug = slugify(shop_name)
            owner_slug = slugify(owner_name)
            timestamp = int(timezone.now().timestamp())

            db_name = f"{shop_slug}_{owner_slug}_{timestamp}"

            # ✅ 2. CREATE SHOP REGISTRY
            shop = ShopRegistry.objects.create(
                shop_name=shop_name,
                owner_name=owner_name,
                email=email,
                db_name=db_name
            )

            # ✅ 3. CREATE SUBSCRIPTION
            plan = SubscriptionPlan.objects.get(id=plan_id)
            start_date = timezone.now().date()
            end_date = start_date + timedelta(days=plan.duration_days)

            Subscription.objects.create(
                shop=shop,
                plan=plan,
                start_date=start_date,
                end_date=end_date,
                amount_paid=plan.price
            )

            # ✅ 4. CREATE SHOP DATABASE + MIGRATE
            create_shop_database(db_name)

            # ✅ 5. CREATE SHOP LOGIN USER
            password = get_random_string(10)
            User.objects.create_user(
                username=email,
                email=email,
                password=password
            )

            message = (
                f"Shop created successfully.\n\n"
                f"Username: {email}\n"
                f"Password: {password}\n"
                f"Database: {db_name}"
            )

        except Exception as e:
            error = f"Error creating shop: {str(e)}"

    return render(
        request,
        "master/add_shop.html",
        {
            "plans": plans,
            "message": message,
            "error": error
        }
    )

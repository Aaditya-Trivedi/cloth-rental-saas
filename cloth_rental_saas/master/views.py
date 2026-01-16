from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import ShopRegistry, Subscription, SubscriptionPlan

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

    if request.method == "POST":
        shop_name = request.POST.get("shop_name")
        owner_name = request.POST.get("owner_name")
        email = request.POST.get("email")
        plan_id = request.POST.get("plan")

        # 1️⃣ Create unique DB name
        db_name = f"shop_{ShopRegistry.objects.count() + 1}"

        # 2️⃣ Create shop registry entry
        shop = ShopRegistry.objects.create(
            shop_name=shop_name,
            owner_name=owner_name,
            email=email,
            db_name=db_name
        )

        # 3️⃣ Create subscription
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

        # 4️⃣ Create shop database + tables
        create_shop_database(db_name)

        # 5️⃣ Create login user for shop
        password = User.objects.make_random_password()
        User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        message = f"Shop created successfully. Login password: {password}"

    return render(
        request,
        "master/add_shop.html",
        {"plans": plans, "message": message}
    )
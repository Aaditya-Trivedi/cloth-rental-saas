from django.contrib import admin
from .models import ShopRegistry, SubscriptionPlan, Subscription

@admin.register(ShopRegistry)
class ShopRegistryAdmin(admin.ModelAdmin):
    list_display = ("shop_name", "owner_name", "email", "db_name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("shop_name", "owner_name", "email")


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "duration_days", "price")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("shop", "plan", "start_date", "end_date", "amount_paid", "is_active")
    list_filter = ("is_active",)
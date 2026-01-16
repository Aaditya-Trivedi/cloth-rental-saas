from django.db import models
from datetime import date

class ShopRegistry(models.Model):
    shop_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    db_name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    duration_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name



class Subscription(models.Model):
    shop = models.OneToOneField("ShopRegistry", on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)

    is_active = models.BooleanField(default=True)

    def is_valid(self):
        return self.is_active and self.end_date >= date.today()

    def __str__(self):
        return f"{self.shop.shop_name} - {self.plan.name}"
from django.db import models
from .barcode_utils import generate_barcode

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Cloth(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    cloth_code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    rent_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    barcode_image = models.ImageField(upload_to="barcodes/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.barcode_image:
            barcode_path = generate_barcode(self.cloth_code)
            self.barcode_image = barcode_path
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cloth_code

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Rental(models.Model):
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    rent_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)

    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    STATUS_CHOICES = [
        ("RENTED", "Rented"),
        ("RETURNED", "Returned"),
        ("OVERDUE", "Overdue"),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="RENTED")

    def __str__(self):
        return f"{self.cloth.cloth_code} - {self.status}"
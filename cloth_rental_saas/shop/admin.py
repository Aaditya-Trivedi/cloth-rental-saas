from django.contrib import admin
from .models import Category, SubCategory, Cloth, Customer, Rental

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Cloth)
admin.site.register(Customer)
admin.site.register(Rental)
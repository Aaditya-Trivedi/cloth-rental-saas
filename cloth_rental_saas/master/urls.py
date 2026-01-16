from django.urls import path
from .views import admin_dashboard, shop_list, toggle_shop

urlpatterns = [
    path("admin-panel/", admin_dashboard, name="admin_dashboard"),
    path("admin-panel/shops/", shop_list, name="admin_shops"),
    path("admin-panel/shop-toggle/<int:shop_id>/", toggle_shop, name="toggle_shop"),
]
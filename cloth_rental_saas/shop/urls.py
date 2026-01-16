from django.urls import path
from .views import (
    dashboard, rent_cloth, return_cloth,
    inventory_report, rented_report,
    overdue_report, fine_report
)

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("rent/", rent_cloth, name="rent"),
    path("return/", return_cloth, name="return"),

    path("reports/inventory/", inventory_report, name="inventory_report"),
    path("reports/rented/", rented_report, name="rented_report"),
    path("reports/overdue/", overdue_report, name="overdue_report"),
    path("reports/fine/", fine_report, name="fine_report"),
]
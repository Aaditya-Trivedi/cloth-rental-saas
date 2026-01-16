from django.urls import path
from .views import dashboard, rent_cloth

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('rent/', rent_cloth, name='rent'),
]
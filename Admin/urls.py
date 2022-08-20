from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('dashboard-chart/', Dashboard_Charts.as_view(), name='dashboard-charts'),
    path('sadsadsad/', dfdsfdsf.as_view(), name='dashboard-csadsadsaharts'),
]

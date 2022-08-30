from django.urls import path
from .views import *

urlpatterns = []

dashboard_urls = [
    ## List
    path('dashboard/request/list/', ContactRequestListView.as_view(), name='contract-request-list'),
    path('dashboard/request/delete/<int:pk>/', ContactRequestDeleteView.as_view(), name='contract-request-delete'),

    ## Forms
    path('dashboard/request/', ContactRequestView.as_view(), name='contract-request'),
    path('dashboard/request/<int:pk>/', ContactRequestView.as_view(),
         name='contract-request'),
]

urlpatterns += dashboard_urls

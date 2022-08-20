from django.urls import path
from .views import *

urlpatterns = []

dashboard_urls = [
    path('dashboard/staff/users/', StaffUserListView.as_view(), name='staff-users'),
    path('dashboard/staff/users/create/', StaffUserCreateView.as_view(), name='staff-users-create'),
    path('dashboard/staff/users/delete/<int:pk>/', StaffUserDeleteView.as_view(), name='staff-users-delete'),
    path('dashboard/staff/users/update/<int:pk>/', StaffUserUpdateView.as_view(), name='staff-users-update'),

    path('dashboard/profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/change/password/', ChangePasswordView.as_view(), name='change-password'),
    path('dashboard/change/avatar/', ChangeAvatarView.as_view(), name='change-avatar'),
]

urlpatterns += dashboard_urls

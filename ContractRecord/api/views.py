import requests
from django.conf import settings
from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from Auth.models import Code
from Sms.helpers import send_sms
from .serializers import *
from ..models import *
from rest_framework.decorators import action


class ContactRequestViewSet(viewsets.ModelViewSet):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.none()
        return qs

    def get_permissions(self):
        if self.action != 'create':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

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
        if self.action not in ['create', 'get_professional_investment_list']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(
        detail=False,
        methods=['get'],
        url_path='professional_investments',
    )
    def get_professional_investment_list(self, request):
        if request.GET.get('type') != 'legal':
            data = [{'id': item[0], 'name': item[1]} for item in PROFESSIONAL_INVETMENT_CHOICES[0:5]]
        else:
            data = [{'id': item[0], 'name': item[1]} for item in PROFESSIONAL_INVETMENT_CHOICES[5:]]

        return Response(data)

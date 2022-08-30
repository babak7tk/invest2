from dataclasses import fields
import requests
from django.conf import settings
from rest_framework import serializers
from django.urls import resolve
from Auth.models import Code
from Sms.helpers import send_sms
from User.api.serializers import UserSerializer
from utils.validator import validate_file_required
from ..models import *
from django_jalali.serializers.serializerfield import JDateField


class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = '__all__'

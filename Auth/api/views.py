import requests
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet
from Auth.api.serializers import *
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthVS(GenericViewSet):
    # Send Local Verification Code (ResetPassword, ...)
    @action(
        methods=["get", "post"],
        detail=False,
        url_path="code/send",
        serializer_class=CodeSerializer,
    )
    def code_send(self, request):
        serializer = self.serializer_class(
            data=request.data, **{'request': request})
        serializer.is_valid(True)
        obj = serializer.save()
        phone = serializer.data['phone']

        if obj:
            return Response({'message': 'پیامک حاوی کد تایید با موفقیت ارسال شد.', 'phone': phone}, 200)
        else:
            return Response(
                {'error': 'خطایی هنگام ارسال پیامک حاوی کد یکبار مصرف پیش آمده است! لطفا دوباره امتحان کنید.'}, 400)

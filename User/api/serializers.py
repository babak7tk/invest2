from rest_framework import serializers
from ..models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_staff', 'is_superuser']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['avatar'] = instance.get_avatar()
        return rep

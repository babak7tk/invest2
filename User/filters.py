import django_filters as filters
from django.db.models import Q, Value
from django.db.models.functions import Concat
from unidecode import unidecode


class UserFilters(filters.FilterSet):
    search = filters.CharFilter(method="search_filter")
    type = filters.CharFilter(method="type_filter")
    limit = filters.CharFilter(method="limit_filter")

    @staticmethod
    def search_filter(qs, name, value):
        qs = qs.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(phone__icontains=value)
        ).distinct()
        return qs

    @staticmethod
    def limit_filter(qs, name, value):
        try:
            qs = qs.distinct()[:int(unidecode(value))]
        except:
            pass
        return qs

    @staticmethod
    def type_filter(qs, name, value):
        if value == 'user':
            qs = qs.filter(Q(teacher_profile__isnull=True) & Q(student_profile__isnull=True))
        elif value == 'teacher':
            qs = qs.filter(teacher_profile__isnull=False)
            print(qs)
        elif value == 'student':
            qs = qs.filter(student_profile__isnull=False)
        return qs


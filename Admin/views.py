from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

from utils.mixins import VerifiedUserMixin

User = get_user_model()


class Dashboard(VerifiedUserMixin, TemplateView):
    template_name = "admin_app/admin/admin-dashboard.html"

class Dashboard_Charts(VerifiedUserMixin, TemplateView):
    template_name = "admin_app/admin/dashboard-charts.html"


class dfdsfdsf(TemplateView):
    template_name = "admin_app/admin/test.html"
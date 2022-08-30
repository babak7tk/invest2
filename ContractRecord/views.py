from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, resolve
from django.views.generic import UpdateView, ListView, DeleteView
from ContractRecord.forms import *
from ContractRecord.models import *
from utils.helpers import get_client_ip
from utils.mixins import VerifiedUserMixin, StaffUserRequiredMixin
from django.views.generic import FormView

User = get_user_model()


class ContactRequestView(FormView):
    form_class = ContactRequestForm
    template_name = "contract_records/admin/form.html"
    success_url = reverse_lazy("dashboard")
    model = ContactRequest

    def get_object(self):
        user = self.request.user
        if self.kwargs.get("pk") and user.is_staff:
            return get_object_or_404(ContactRequest, pk=self.kwargs.get("pk"))
        return None

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        kwargs.update({'object': self.get_object()})
        kwargs.update(
            {"professional_investment_choices": PROFESSIONAL_INVETMENT_CHOICES})
        kwargs.update({"evidence_investment_choices": EVIDENCE_CHOICES})
        kwargs.update(
            {"review_end_proccess_choices": REVIEW_END_PROCCESS_CHOICES})
        return super().get_context_data(**kwargs)


class ContactRequestListView(StaffUserRequiredMixin, ListView):
    model = ContactRequest
    paginate_by = settings.PAGINATION_NUMBER
    template_name = 'contract_records/admin/list.html'


class ContactRequestDeleteView(StaffUserRequiredMixin, DeleteView):
    model = ContactRequest
    template_name = 'contract_records/admin/list.html'
    success_url = reverse_lazy("contract-request-approved-list")

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return self.success_url

    def dispatch(self, *args, **kwargs):
        resp = super().dispatch(*args, **kwargs)
        messages.success(self.request, 'آیتم مورد نظر با موفقیت حدف شد.')
        return resp

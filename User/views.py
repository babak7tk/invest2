from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, ListView, CreateView, DeleteView

from utils.mixins import VerifiedUserMixin, SuperUserRequiredMixin
from .forms import *

""" Staff Users crud """


class StaffUserListView(SuperUserRequiredMixin, ListView):
    model = User
    paginate_by = settings.PAGINATION_NUMBER
    template_name = 'users/admin/users/list.html'
    queryset = User.objects.filter(is_staff=True)


class StaffUserCreateView(SuperUserRequiredMixin, CreateView):
    model = User
    template_name = 'users/admin/users/form.html'
    form_class = StaffUserForm
    success_url = reverse_lazy('staff-users')


class StaffUserUpdateView(SuperUserRequiredMixin, UpdateView):
    model = User
    template_name = 'users/admin/users/form.html'
    form_class = StaffUserForm
    success_url = reverse_lazy('staff-users')


class StaffUserDeleteView(SuperUserRequiredMixin, DeleteView):
    model = User
    template_name = 'users/admin/users/form.html'
    success_url = reverse_lazy("staff-users")

    def dispatch(self, *args, **kwargs):
        resp = super().dispatch(*args, **kwargs)
        messages.success(self.request, 'آیتم مورد نظر با موفقیت حدف شد.')
        return resp


##


class ChangePasswordView(VerifiedUserMixin, View):
    form = SetPasswordForm
    template_name = 'users/admin/users/change_password.html'
    success_url = reverse_lazy("dashboard")

    def get(self, req):
        context = {"form": self.form(req.user), 'object': req.user}
        return render(req, self.template_name, context)

    def post(self, req):
        form = SetPasswordForm(req.user, req.POST)
        if form.is_valid():
            user = form.save()
            messages.success(req, 'رمزعبور با موفقیت تغییر داده شد.')
            return redirect(self.success_url)
        return render(req, self.template_name, context={"form": form})


class ChangeAvatarView(VerifiedUserMixin, UpdateView):
    template_name = "users/admin/users/form.html"
    model = User
    fields = ['avatar']
    success_url = reverse_lazy("dashboard")

    def get_object(self, queryset=None):
        return self.request.user


class ProfileView(VerifiedUserMixin, UpdateView):
    template_name = "users/admin/users/form.html"
    model = User
    fields = ['avatar']
    success_url = reverse_lazy("profile")

    def get_context_data(self, **kwargs):
        kwargs.update({'is_profile': True})
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        messages.success(request, 'اطلاعات شما با موفقیت ویرایش شد.')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

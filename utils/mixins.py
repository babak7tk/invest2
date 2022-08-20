from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from datetime import timedelta
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse_lazy

from Auth.models import Code


class PermissionMixin(object):
    user = None
    permissions = []
    redirect_url = reverse_lazy('login')

    def get_redirect_url(self):
        # Check if redirect_url is set on request GET param
        self.redirect_url += '?redirect_url={}'.format(self.request.path)
        return self.redirect_url

    def dispatch(self, *args, **kwargs):
        self.user = self.request.user

        # Then check if the user has correct type
        if not self.user.is_authenticated:
            return HttpResponseRedirect(self.get_redirect_url())

        # Then check if user is active or idk ex: shop is active or ...
        if not self.check_active():
            return HttpResponseForbidden()

        # Authorization checks here
        if not self.check_permissions():
            return HttpResponseForbidden()

        return super().dispatch(*args, **kwargs)

    def check_permissions(self):
        if self.user.is_superuser:
            return True

        for permission in self.permissions:
            if any(permission in p for p in self.user.permissions):
                return True

        if self.user.is_staff:
            return True
        return False

    def check_active(self):
        return self.user.is_active


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


class StaffUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff


class AnonymousUserMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('dashboard'))
        else:
            return super().dispatch(request, *args, **kwargs)


class VerifiedUserMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('/login?next=' + str(request.path))


class CheckPasswordResetExpirationMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.session.has_key('reset_password_code'):
            reset_password = Code.objects.filter(code=request.session['reset_password_code']).first()
            if reset_password:
                today = timezone.now()
                expiration = reset_password.created_at + timedelta(minutes=15)
                if today < expiration:
                    return super().dispatch(request, *args, **kwargs)

        try:
            del request.session['reset_password_code']
        except:
            pass
        return redirect('/')

from django.contrib.auth.forms import SetPasswordForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView as LoginViewAuto
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.views.generic.base import View
import requests
from django.forms.forms import NON_FIELD_ERRORS
from config import settings
from utils.mixins import AnonymousUserMixin, CheckPasswordResetExpirationMixin
from .forms import *

def landing(request):
    return redirect(reverse_lazy('contract-request'))

class LoginView(LoginViewAuto):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('dashboard')
    success_url = reverse_lazy('dashboard')
    form_class = LoginForm
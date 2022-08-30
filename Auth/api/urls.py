from django.urls import path, include
# from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("", UserAuthVS, "auth")

urlpatterns = [
    path('', include(router.urls)),
]

from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import MyTokenView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", MyTokenView.as_view()),
]

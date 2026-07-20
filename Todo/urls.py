from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyTokenView, RegisterView, TaskViewSet

# Criando o router
router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", MyTokenView.as_view()),

    # CRUD 
    path("", include(router.urls)),
]

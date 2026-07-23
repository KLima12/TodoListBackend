from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, RegisterView, TaskViewSet, DetalhesViewSet

# Criando o router
router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"detalhes", DetalhesViewSet, basename="detalhes")

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    # CRUD 
    path("", include(router.urls)),
]

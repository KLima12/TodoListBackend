from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView 
from Todo.views import CustomRefreshView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', CustomRefreshView.as_view(), name="token_refesh"),
    path('api/token/verify/', TokenVerifyView.as_view(), name="token_verify"), 
    path('api/', include("Todo.urls")),
]

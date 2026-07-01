from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, MyTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(APIView): 
    def post(self, request): 
        # Request que vem do react
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid(): 
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({ 
                "user": { 
                    "id": user.id, 
                    "email": user.email,
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MyTokenView(TokenObtainPairView): 
    serializer_class = MyTokenSerializer
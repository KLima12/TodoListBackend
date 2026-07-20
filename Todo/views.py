from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, MyTokenSerializer, TaskSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import TodoList
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
    """View para login retornando tokens """
    serializer_class = MyTokenSerializer


class verifyToken(APIView): 
    """
    View para verificar se o token de acesso ainda é válido. 
    Retorna 200 ok se o token for válido, 401 se não for.
    """
    def get(self, request): 
        return Response({ 
            "valid": True, 
            "user": { 
                "id": request.user.id, 
                "email": request.user.email, 
                "username": request.user.name
            }
        }, status=status.HTTP_200_OK)
    
    def post(self, request): 
        return self.get(request)

class TaskViewSet(ModelViewSet): 
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # Aqui só irei mostrar as tarefas do usuário logado
    def get_queryset(self):
        return TodoList.objects.filter(user=self.request.user)
    # Garante que a tarefa criada pertence ao usuário logado.
    def perform_create(self, serializer): 
        serializer.save(user=self.request.user)
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, MyTokenSerializer, TaskSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.conf import settings
from .models import TodoList
class RegisterView(APIView): 
    permission_classes = [AllowAny] # Register público
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
    
class LoginView(APIView):
    permission_classes = [AllowAny] # Público
    # Usamos um Serializer normal para ter controle total dos campos
    def post(self, request): 
        self.permission_classes = [AllowAny]
        serializer = MyTokenSerializer(data=request.data)

        if serializer.is_valid(): 
            return Response(serializer.validated_data,  status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class verifyToken(APIView): 
    """View para verificar se o token ainda é válido."""
    permission_classes = [AllowAny]
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
    
class CustomRefreshView(APIView): 
    """View de refresh customizada"""
    def post(self, request): 
        refresh_token = request.data.get('refresh')

        print("Tentando refresh token...")
        print(f"Refresh token recebido: {refresh_token[:200]}")

        if not refresh_token: 
            print("Refresh token não fornecido")
            return Response( 
                {"detail": "Refresh token é obrigatório"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try: 
            refresh = RefreshToken(refresh_token)

            print("Refresh token válido")

            new_access_token = str(refresh.access_token)

            # Se rotate_refresh_tokens=true, também gera um novo refresh
            new_refresh_token = None
            if settings.SIMPLE_JWT.get("ROTATE_REFRESH_TOKENS",  False): 
                new_refresh_token = str(refresh)
                print("Novo refresh token gerado")

            response_data = { 
                'access': new_access_token
            }

            if new_refresh_token: 
                response_data["refresh"] = new_refresh_token

            print("Token renovados com sucesso!")
            return Response(response_data, status=status.HTTP_200_OK)
        
        except InvalidToken:
            print("❌ Token inválido!")
            return Response(
                {"detail": "Token inválido ou expirado"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except TokenError as e:
            print(f"❌ Erro no token: {str(e)}")
            return Response(
                {"detail": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            print(f"❌ Erro inesperado: {str(e)}")
            import traceback
            traceback.print_exc()  # 👈 Mostra o erro completo no terminal
            return Response(
                {"detail": f"Erro interno: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated] # necessita de autenticação
    serializer_class = TaskSerializer
    

    # Aqui só irei mostrar as tarefas do usuário logado
    def get_queryset(self):
        return TodoList.objects.filter(user=self.request.user)
    # Garante que a tarefa criada pertence ao usuário logado.
    def perform_create(self, serializer): 
        serializer.save(user=self.request.user)
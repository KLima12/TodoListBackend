from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, MyTokenSerializer, TaskSerializer, DetailsSeriaizer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.conf import settings
from .models import TodoList, DetalhesList
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import serializers
class RegisterView(APIView): 
    permission_classes = [AllowAny] # Register público
    def post(self, request): 
        try:
            serializer = RegisterSerializer(data=request.data)
        except Exception as e: 
            print(f"Erro: {e}")

        if not serializer.is_valid(): 
            print(f"Erros de validação: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
        try: 
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
        except Exception as e: 
            print(f"❌ Erro no registro: {str(e)}")
            import traceback
            traceback.print_exc()  # 👈 Mostra erro completo
            
            return Response(
                {"detail": f"Erro interno: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
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

        if not refresh_token: 
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

            response_data = { 
                'access': new_access_token
            }

            if new_refresh_token: 
                response_data["refresh"] = new_refresh_token
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


class DetalhesViewSet(ModelViewSet):
    """
    ViewSet para gerenciar detalhes das tarefas.
    URLs: /api/detalhes/
    """
    serializer_class = DetailsSeriaizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna todos os detalhes das tarefas do usuário"""
        return DetalhesList.objects.filter(todo__user=self.request.user)

    def get_todo(self, todo_id):
        """Valida se a tarefa TODOList existe e pertence ao usuário"""
        return get_object_or_404(
            TodoList, 
            id=todo_id, 
            user=self.request.user
        )

    def perform_create(self, serializer):
        """Cria detalhes para uma tarefa específica"""
        todo_id = self.request.data.get('id')
        
        if not todo_id:
            raise serializers.ValidationError(
                {"task_id": "Este campo é obrigatório."}
            )
        
        todo = self.get_todo(todo_id)

        # Verificando se já tem detalhes na tarefa.

        if hasattr(todo, "detalhe"): 
            raise serializers.ValidationError(
                "Esta tarefa já possui detalhes"
            )

        # Serializer ele já tem o dado do que vem do request, mas nao tem o do todo.
        serializer.save(data=todo)

    def perform_update(self, serializer):
        """Atualiza detalhes existentes"""
        todo_id = self.request.data.get('todo_id')
        
        if todo_id: 
            todo = self.get_todo(todo_id)

            serializer.save(todo=todo)
        else: 
            serializer.save()
   
    @action(detail=True, methods=['patch'])
    def toggle_concluido(self, request, pk=None):
        """
        Alterna o status de concluído
        """
        detalhes = self.get_object() # Pegando DetalhesList
        detalhes.concluido = not detalhes.concluido
        detalhes.save()

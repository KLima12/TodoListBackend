from django.contrib.auth.models import User
from .models import TodoList
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User
        fields = ["username", "email", "password"]
        # Ocultando a senha
        extra_kwargs = { 
            "password": {"write_only": True}
        }

    # Aqui vou fazer um hash na senha
    def create(self, validated_data): 
        return User.objects.create_user(**validated_data)
    
class MyTokenSerializer(serializers.Serializer):
    # Usamos um Serializer normal para ter controle total dos campos
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # 1. Busca o usuário pelo e-mail
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("Usuário não encontrado.")

        # 2. Autentica usando o username real e a senha
        authenticated_user = authenticate(username=user.username, password=password)

        if authenticated_user is None:
            raise AuthenticationFailed("Senha incorreta.")

        if not authenticated_user.is_active:
            raise AuthenticationFailed("Esta conta está inativa.")

        # 3. Geramos os tokens manualmente para o usuário autenticado
        refresh = RefreshToken.for_user(authenticated_user)

        # 4. Retornamos o dicionário com os dados que a View vai entregar
        return {
            "email": authenticated_user.email,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

class TaskSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = TodoList
        fields = ['id','nome', 'favorito', 'quantidade']
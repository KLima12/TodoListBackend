from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import TodoList
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
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
    """
        Login com email e senha. 
        Verifica senha é válida logo dps libera access token e refresh
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        print(f"🔍 Tentando login com email: {email}")
        
        # Busca o usuário pelo email
        user = User.objects.filter(email=email).first()
        
        if user is None:
            print("❌ Usuário não encontrado")
            raise AuthenticationFailed("Usuário não encontrado.")

        print(f"✅ Usuário encontrado: {user.username}")
        print(f"🔐 Verificando senha...")

        if not check_password(password, user.password):
            print("❌ Senha incorreta!")
            raise AuthenticationFailed("Senha incorreta.")

        if not user.is_active:
            print("❌ Usuário inativo")
            raise AuthenticationFailed("Esta conta está inativa.")

        print("✅ Senha correta! Gerando tokens...")

        # Gera tokens
        refresh = RefreshToken.for_user(user)

        return {
            "email": user.email,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
class TaskSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = TodoList
        fields = ['id','nome', 'favorito', 'quantidade']
        read_only_fields = ['user']  # O user não pode ser alterado via API
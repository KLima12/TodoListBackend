from django.contrib.auth.models import User
from .models import TodoList, DetalhesList
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
class RegisterSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ["email", "password"]
        # Ocultando a senha
        extra_kwargs = { 
            "password": {"write_only": True}
        }

    # Validação se email já está cadastrado
    def validate_email(self,value): 
        if User.objects.filter(email=value).exists(): 
            raise serializers.ValidationError("Este email já está cadastrado")

        return value

    def validate_password(self, value): 
        if len(value) < 6: 
            raise serializers.ValidationError("A senha deve até 6 caracteres")
        return value
    
    # Aqui vou fazer um hash na senha
    def create(self, validated_data): 
        email = validated_data.get("email")
        password = validated_data.get("password")

        user = User.objects.create_user( 
            username=email, 
            email=email, 
            password=password
        )

        return user
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

class DetailsSeriaizer(serializers.ModelSerializer): 
    class Meta: 
        model = DetalhesList
        fields = all
        
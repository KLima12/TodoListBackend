from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate

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
    
class MyTokenSerializer(TokenObtainPairSerializer): 
    username_field = 'email'

    def validate(self, attrs):
        credentials =  {
            "email": attrs.get("email"), 
            "password": attrs.get("password") 
        }

        user = authenticate(**credentials)

        if user is None: 
            raise AuthenticationFailed("Credenciais inválidas.")

        data = super().validate(attrs)

        return data

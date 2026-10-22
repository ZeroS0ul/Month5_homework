import random
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserConfirmCode


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует.")
        return value

    def create(self, validated_data):
      
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_active=False
        )
        
     
        code = UserConfirmCode.generate_code()
        
   
        UserConfirmCode.objects.create(user=user, code=code)
        
     
        print(f"\n--- КОД ПОДТВЕРЖДЕНИЯ ДЛЯ {user.username}: {code} ---\n")
        
        return user


class ConfirmUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        username = data.get('username')
        code = data.get('code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким именем не найден.")

        try:
            confirm_obj = UserConfirmCode.objects.get(user=user)
        except UserConfirmCode.DoesNotExist:
            raise serializers.ValidationError("Код подтверждения для этого пользователя не найден.")

        if confirm_obj.code != code:
            raise serializers.ValidationError("Неверный код подтверждения.")

        data['user'] = user
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
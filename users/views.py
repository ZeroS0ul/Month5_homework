from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, ConfirmUserSerializer, LoginSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Регистрация прошла успешно. Проверьте консоль сервера для получения 6-значного кода подтверждения.",
                    "username": user.username
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmUserAPIView(APIView):
    def post(self, request):
        serializer = ConfirmUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
       
            user.is_active = True
            user.save()
            
            
            user.confirm_code.delete()
            
            return Response({"message": "Пользователь успешно подтвержден и активирован!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active:
                    return Response({"error": "Аккаунт не подтвержден. Сначала подтвердите аккаунт кодом."}, status=status.HTTP_403_FORBIDDEN)
                
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            
            return Response({"error": "Неверное имя пользователя или пароль."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации пользователя.

    Используется для создания нового пользователя
    с проверкой пароля и его подтверждения.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        """
        Проверяет совпадение паролей.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        """
        Создаёт пользователя с хешированным паролем.
        """
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user

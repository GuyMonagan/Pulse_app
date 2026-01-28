from rest_framework import generics
from .models import CustomUser
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    API для регистрации нового пользователя.
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

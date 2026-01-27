from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Habit
from .serializers import HabitSerializer
from rest_framework.pagination import PageNumberPagination

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Только автор может редактировать/удалять.
    Остальные могут только GET (если публично).
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем GET/HEAD/OPTIONS всем
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class HabitPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = HabitPagination

    def get_queryset(self):
        if self.request.query_params.get('public') == 'true':
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


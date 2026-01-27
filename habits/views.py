from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination

from .models import Habit
from .serializers import HabitSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Редактировать и удалять может только владелец.
    Читать можно всем (если привычка публичная).
    """

    def has_object_permission(self, request, view, obj):
        # GET / HEAD / OPTIONS — разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # PUT / PATCH / DELETE — только владелец
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
        """
        - /api/habits/               -> привычки текущего пользователя
        - /api/habits/?public=true   -> публичные привычки всех пользователей
        """
        if self.request.query_params.get('public') == 'true':
            return Habit.objects.filter(is_public=True)

        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

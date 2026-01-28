from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination

from .models import Habit
from .serializers import HabitSerializer
from habits.services import calculate_next_reminder
from .models import models


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение на доступ к привычке.

    Редактировать и удалять может только владелец.
    Просмотр разрешён всем (при наличии доступа к объекту).
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет права доступа к конкретному объекту.
        """
        # GET / HEAD / OPTIONS — разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # PUT / PATCH / DELETE — только владелец
        return obj.user == request.user


class HabitPagination(PageNumberPagination):
    """
    Пагинация для списка привычек.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class HabitViewSet(viewsets.ModelViewSet):
    """
    API для работы с привычками.

    Поддерживает:
    - получение списка привычек
    - создание, редактирование и удаление привычек пользователя
    - просмотр публичных привычек
    """
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = HabitPagination

    def get_queryset(self):
        """
        Возвращает список привычек в зависимости от параметров запроса.

        Поведение:
        - без параметров — привычки текущего пользователя + публичные
        - ?public=true — только публичные привычки всех пользователей
        """
        user = self.request.user
        if self.request.query_params.get('public') == 'true':
            return Habit.objects.filter(is_public=True).order_by('id')

        return Habit.objects.filter(models.Q(user=user) | models.Q(is_public=True)).order_by('id')

    def perform_create(self, serializer):
        """
        Создаёт привычку и рассчитывает напоминание при необходимости.
        """
        habit = serializer.save(user=self.request.user)

        if habit.is_reminder_enabled:
            habit.next_reminder = calculate_next_reminder(habit)
            habit.save(update_fields=['next_reminder'])

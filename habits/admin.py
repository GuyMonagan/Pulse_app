from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    # Что видим в таблице
    list_display = ('action', 'user', 'get_timezone', 'time', 'next_reminder', 'is_reminder_enabled')
    # По каким полям фильтруем (справа)
    list_filter = ('is_reminder_enabled', 'is_pleasant', 'user__timezone')
    # По чему ищем
    search_fields = ('action', 'user__username')

    # Метод, чтобы вытащить таймзону юзера в таблицу привычек
    @admin.display(description='Часовой пояс')
    def get_timezone(self, obj):
        return obj.user.timezone

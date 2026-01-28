from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from habits.models import Habit  # импортируем модель привычек


# Это позволит редактировать привычки прямо внутри юзера
class HabitInline(admin.TabularInline):
    model = Habit
    extra = 0  # чтобы не плодились пустые строки


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = [HabitInline]  # Добавляем список привычек вниз страницы юзера

    # Поля, которые будут видны в списке всех юзеров
    list_display = ['username', 'email', 'timezone', 'telegram_chat_id', 'is_staff']

    # Поля, которые можно редактировать внутри формы
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('timezone', 'telegram_chat_id')}),
    )

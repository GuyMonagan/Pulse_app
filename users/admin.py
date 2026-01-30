from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from habits.models import Habit
from .models import CustomUser


class HabitInline(admin.TabularInline):
    model = Habit
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    inlines = [HabitInline]

    # Список пользователей
    list_display = (
        "email",
        "timezone",
        "telegram_chat_id",
        "is_staff",
        "is_active",
    )

    ordering = ("email",)
    search_fields = ("email",)

    # Поля формы редактирования пользователя
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Дополнительно",
            {"fields": ("timezone", "telegram_chat_id")},
        ),
        (
            "Важные даты",
            {"fields": ("last_login", "date_joined")},
        ),
    )

    # Поля при создании пользователя в админке
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

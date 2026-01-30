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

    list_display = (
        "email",
        "telegram_username",
        "timezone",
        "is_staff",
        "is_active",
    )
    ordering = ("email",)
    search_fields = ("email", "telegram_username")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Персональная информация",
            {"fields": ("telegram_username", "telegram_chat_id", "timezone")},
        ),
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
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password", "is_staff", "is_active"),
            },
        ),
    )

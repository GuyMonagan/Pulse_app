from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "user",
        "get_timezone",
        "time",
        "next_reminder",
        "is_reminder_enabled",
    )
    list_filter = ("is_reminder_enabled", "is_pleasant", "user__timezone")
    # Ищем по email и тг-нику, так как username удален
    search_fields = ("action", "user__email", "user__telegram_username")


    @admin.display(description="Часовой пояс")
    def get_timezone(self, obj):
        return obj.user.timezone

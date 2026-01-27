from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        is_pleasant = data.get('is_pleasant')
        reward = data.get('reward')
        related_habit = data.get('related_habit')
        duration = data.get('duration')
        periodicity = data.get('periodicity')

        # Нельзя указывать и reward, и related_habit
        if reward and related_habit:
            raise serializers.ValidationError("Укажите только награду или связанную привычку, не оба поля.")

        # Приятная привычка не может иметь награду или связанную привычку
        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError("Приятная привычка не может иметь награду или связанную привычку.")

        # Связанная привычка может быть только приятной
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной.")

        # Время выполнения <= 120
        if duration and duration > 120:
            raise serializers.ValidationError("Время выполнения не должно превышать 120 секунд.")

        # Периодичность не больше 7
        if periodicity and periodicity > 7:
            raise serializers.ValidationError("Периодичность не может быть более 7 дней.")

        return data

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from habits.models import Habit


class HabitAPITest(APITestCase):
    """
    Тесты API привычек.

    Проверяет авторизацию, создание, пагинацию
    и доступ к публичным привычкам.
    """
    def setUp(self):
        """Создаёт пользователя и URL для тестов привычек."""
        self.user = CustomUser.objects.create_user(username='api_user', password='password123')
        # Получаем URL
        self.login_url = reverse('token_obtain_pair')
        self.habit_list_url = reverse('habit-list')

    def test_get_habits_unauthorized(self):
        """Неавторизованный пользователь не видит список привычек."""
        response = self.client.get(self.habit_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_habit_via_api(self):
        """Создание привычки через API авторизованным пользователем."""
        self.client.force_authenticate(user=self.user)  # Авторизуем юзера
        data = {
            "action": "API Habit",
            "place": "Online",
            "time": "15:00:00",
            "duration": 60,
            "is_reminder_enabled": True
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.filter(action="API Habit").count(), 1)

    def test_habit_pagination(self):
        """Проверяем, что пагинация работает и выдает правильный формат"""
        # Создаем 6 привычек (пагинация по 5)
        for i in range(6):
            Habit.objects.create(
                user=self.user, action=f"Habit {i}",
                place="Home", time="12:00:00", duration=60
            )

        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/habits/')

        # Проверяем структуру ответа пагинации
        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('count', response.data)

    def test_public_habit_visibility(self):
        """Чужую ПУБЛИЧНУЮ привычку можно видеть, но нельзя менять"""
        other_user = CustomUser.objects.create_user(username='guest', password='123')
        public_habit = Habit.objects.create(
            user=self.user, action="Public Action",
            is_public=True, time="12:00:00", duration=60
        )

        self.client.force_authenticate(user=other_user)

        # Добавляем параметр, который ждет вьюха
        response = self.client.get('/api/habits/?public=true')
        actions = [h['action'] for h in response.data['results']]
        self.assertIn("Public Action", actions)

        # Проверяем редактирование (должно быть запрещено 403)
        response = self.client.patch(f'/api/habits/{public_habit.id}/', {"action": "Hacked"})
        self.assertEqual(response.status_code, 403)  # Или 404, зависит от твоих Permission

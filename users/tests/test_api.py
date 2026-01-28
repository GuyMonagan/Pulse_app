from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser


class UserAPITest(APITestCase):
    """
    Тесты пользовательского API.

    Проверяет регистрацию пользователя через API.
    """
    def setUp(self):
        """Создаёт тестового пользователя и основные URL."""
        self.user = CustomUser.objects.create_user(username='api_user', password='password123')
        self.login_url = reverse('token_obtain_pair')
        self.habit_list_url = reverse('habit-list')

    def test_registration(self):
        """Тест регистрации через API"""
        data = {
            "username": "tester_new",
            "email": "test@example.com",
            "password": "StrongPass123",
            "password2": "StrongPass123",
            "timezone": "Asia/Tashkent"
        }

        response = self.client.post('/api/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

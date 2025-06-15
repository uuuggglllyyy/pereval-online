import json
from datetime import time

from django.contrib.sites import requests
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from pereval.models import User, Pereval, Coords, Level, Image

API_URL = "http://127.0.0.1:8000/submitData/"


def test_valid_data():
    """Тест с корректными данными"""
    print("\n=== Тест с валидными данными ===")

    data = {
        "beauty_title": "пер. ",
        "title": "Тестовый перевал",
        "other_titles": "Тест-Перевал",
        "connect": "тестовое соединение",
        "add_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "user": {
            "email": f"test_{int(time.time())}@example.com",
            "last_name": "Тестов",
            "first_name": "Тест",
            "patronymic": "Тестович",
            "phone": "+7 000 000 00 00"
        },
        "coords": {
            "latitude": "45.0000",
            "longitude": "90.0000",
            "height": "2500"
        },
        "level": {
            "winter": "",
            "summer": "1А",
            "autumn": "1А",
            "spring": ""
        },
        "images": [
            {"file_path": "test_image1.jpg", "title": "Тест фото 1"},
            {"file_path": "test_image2.jpg", "title": "Тест фото 2"}
        ]
    }

    response = requests.post(API_URL, json=data)
    print(f"Status Code: {response.status_code}")
    print("Response:", json.dumps(response.json(), indent=2, ensure_ascii=False))

    assert response.status_code == 200
    assert response.json().get('id') is not None
    print("✅ Тест пройден успешно")
    return response.json()['id']


def test_invalid_data():
    """Тест с неполными данными"""
    print("\n=== Тест с невалидными данными ===")

    invalid_data = {
        "title": "Неполные данные",
        "user": {"email": "invalid@example.com"}
        # Нет обязательных полей: coords, level
    }

    response = requests.post(API_URL, json=invalid_data)
    print(f"Status Code: {response.status_code}")
    print("Response:", json.dumps(response.json(), indent=2, ensure_ascii=False))

    assert response.status_code == 400
    assert 'message' in response.json()
    print("✅ Тест пройден успешно (корректно отловил ошибку)")


def test_db_integration(pereval_id):
    """Проверка сохранения в БД"""
    print("\n=== Проверка записи в БД ===")

    # Здесь должна быть логика проверки вашей БД
    # Например, запрос к Django ORM или прямой SQL-запрос
    print(f"Проверьте в админке или БД запись с ID: {pereval_id}")
    print("Убедитесь, что:")
    print("- Все поля сохранены корректно")
    print("- Фотографии привязаны к перевалу")
    print("- Координаты сохранены правильно")


if __name__ == "__main__":
    print("=== Начало тестирования метода submitData ===")

    # Тест 1: Валидные данные
    pereval_id = test_valid_data()

    # Тест 2: Невалидные данные
    test_invalid_data()

    # Тест 3: Проверка БД
    test_db_integration(pereval_id)

    print("\n=== Тестирование завершено ===")


class PerevalAPITestCase(APITestCase):
    def setUp(self):
        """Создание тестовых данных"""
        self.client = APIClient()

        # Создаем тестового пользователя
        self.user = User.objects.create(
            email='test@mail.com',
            fam='Иванов',
            name='Иван',
            otc='Иванович',
            phone='+79999999999'
        )

        # Создаем координаты
        self.coords = Coords.objects.create(
            latitude=45.3842,
            longitude=7.1525,
            height=1200
        )

        # Создаем уровень сложности
        self.level = Level.objects.create(
            winter='',
            summer='1А',
            autumn='1А',
            spring=''
        )

        # Создаем перевал
        self.pereval = Pereval.objects.create(
            beauty_title='пер.',
            title='Пхия',
            other_titles='Триев',
            connect='',
            add_time='2021-09-22 13:18:13',
            user=self.user,
            coords=self.coords,
            level=self.level,
            status='new'
        )

        # Создаем изображения
        self.image1 = Image.objects.create(
            pereval=self.pereval,
            data='https://example.com/image1.jpg',
            title='Седловина'
        )
        self.image2 = Image.objects.create(
            pereval=self.pereval,
            data='https://example.com/image2.jpg',
            title='Подъем'
        )

        # Данные для POST/PATCH запросов
        self.valid_data = {
            "beauty_title": "пер. ",
            "title": "Тестовый перевал",
            "other_titles": "Тест",
            "connect": "",
            "add_time": "2023-01-01 12:00:00",
            "user": {
                "email": "test2@mail.com",
                "fam": "Петров",
                "name": "Петр",
                "otc": "Петрович",
                "phone": "+78888888888"
            },
            "coords": {
                "latitude": "46.3842",
                "longitude": "8.1525",
                "height": "1300"
            },
            "level": {
                "winter": "",
                "summer": "1Б",
                "autumn": "1А",
                "spring": ""
            },
            "images": [
                {
                    "data": "https://example.com/test1.jpg",
                    "title": "Тест 1"
                },
                {
                    "data": "https://example.com/test2.jpg",
                    "title": "Тест 2"
                }
            ]
        }

    # Тест для GET /submitData/<id>
    def test_get_pereval_detail(self):
        url = reverse('pereval-detail', kwargs={'pk': self.pereval.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.pereval.id)
        self.assertEqual(response.data['title'], 'Пхия')
        self.assertEqual(response.data['status'], 'new')
        self.assertEqual(len(response.data['images']), 2)

    # Тест для PATCH /submitData/<id> (успешное обновление)
    def test_update_pereval_success(self):
        url = reverse('pereval-update', kwargs={'pk': self.pereval.id})
        update_data = {
            "title": "Обновленное название",
            "other_titles": "Обновленный другой титул",
            "level": {
                "summer": "2А"
            }
        }

        response = self.client.patch(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 1)
        self.assertEqual(response.data['message'], 'Запись успешно обновлена')

        # Проверяем, что данные действительно обновились
        updated_pereval = Pereval.objects.get(id=self.pereval.id)
        self.assertEqual(updated_pereval.title, 'Обновленное название')
        self.assertEqual(updated_pereval.level.summer, '2А')

    # Тест для PATCH /submitData/<id> (попытка изменить пользователя)
    def test_update_pereval_user_change_fail(self):
        url = reverse('pereval-update', kwargs={'pk': self.pereval.id})
        update_data = {
            "user": {
                "email": "new@mail.com"
            }
        }

        response = self.client.patch(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['state'], 0)
        self.assertEqual(response.data['message'], 'Нельзя изменять данные пользователя')

    # Тест для PATCH /submitData/<id> (попытка изменить не-new запись)
    def test_update_non_new_pereval_fail(self):
        # Меняем статус перевала
        self.pereval.status = 'accepted'
        self.pereval.save()

        url = reverse('pereval-update', kwargs={'pk': self.pereval.id})
        update_data = {"title": "Новое название"}

        response = self.client.patch(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['state'], 0)
        self.assertIn('статус не "new"', response.data['message'])

    # Тест для GET /submitData/?user__email=<email> (успешный запрос)
    def test_get_user_perevals_success(self):
        url = reverse('user-perevals-list') + '?user__email=test@mail.com'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['email'], 'test@mail.com')

    # Тест для GET /submitData/?user__email=<email> (пустой результат)
    def test_get_user_perevals_empty(self):
        url = reverse('user-perevals-list') + '?user__email=notexist@mail.com'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # Тест для GET /submitData/?user__email=<email> (без параметра)
    def test_get_user_perevals_no_param(self):
        url = reverse('user-perevals-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

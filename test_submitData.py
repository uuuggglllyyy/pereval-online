import requests
import json
import time

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
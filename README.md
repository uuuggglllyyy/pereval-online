# Pereval-Online 🌄

**REST API для учёта данных о горных перевалах**  
Проект позволяет туристам добавлять информацию о перевалах и просматривать существующие записи.

---

## 🔹 **API Endpoints**

| Метод | URL                                                                          | Описание                           | Статус       |
|-------|------------------------------------------------------------------------------|------------------------------------|--------------|
| GET   | `/`                                                                          | Перенаправление на `/submitData/`  | ✅ Реализован |
| POST  | `/submitData/`                                                               | Добавить новый перевал             | ✅ Реализован |
| GET   | `/submitData/<int:pk>/`                                                      | Получить перевал по ID             | ✅ Реализован |
| GET   | `/submitData/swagger/`<br/> `/submitData/schema/` <br/> `/submitData/redoc/` | Интерактивная документация Swagger | ✅ Реализован |

---

## 🔹 **Детализация эндпоинтов**

### 1. Добавление перевала (`POST /submitData/`)
**Пример запроса:**
```json
{
    "beauty_title": "пер. ",
    "title": "Пхия",
    "other_titles": "Триев",
    "connect": "",
    "add_time": "2021-09-22 13:18:13",
    "user": {
        "email": "qwerty@mail.ru",
        "last_name": "Пупкин",
        "first_name": "Василий",
        "middle_name": "Иванович",
        "phone": "+7 555 55 55"
    },
    "coords": {
        "latitude": "45.3842",
        "longitude": "7.1525",
        "height": "1200"
    },
    "level": {
        "winter": "",
        "summer": "1А",
        "autumn": "1А",
        "spring": ""
    },
    "images": [
        {"file_path": "седловина.jpg", "title": "Седловина"},
        {"file_path": "подъем.jpg", "title": "Подъём"}
    ]
}
Ответ:

json
{
  "status": 200,
  "message": null,
  "id": 42
}

2. Просмотр перевала (GET /submitData/42/)
Ответ:

json
{
  "id": 42,
  "status": "new",
  "title": "Пхия",
  "user": {
    "email": "user@mail.ru",
    "phone": "+79991234567",
    "last_name": "Иванов"
  },
  "coords": {
    "latitude": 45.3842,
    "longitude": 7.1525
  },
  "images": []
}

Возможные ответы:

Статус	Тело ответа
201	{"status": 201, "id": 123}
400	{"error": "Invalid email format"}
500	{"error": "Database error"}

🔹 Установка

bash
# 1. Клонировать репозиторий
git clone https://github.com/uuuggglllyyy/pereval-online.git

# 2. Установить необходимые библиотеки

# 3. Запустить сервер
python manage.py runserver

🔹 Планируемые обновления
Редактирование данных через PATCH

Фильтрация перевалов по пользователю

Система модерации с изменением статуса

📫 Контакты
Разработчик: uuuggglllyyy
Поддержка: great.egor7288@gmai.com

Полное руководство по использованию приложения pereval

1. Структура проекта
pereval/
├── pereval_api/          # Основное Django-приложение
│   ├── models.py         # Модели базы данных
│   ├── serializers.py    # Сериализаторы для API
│   ├── views.py          # Обработчики запросов
│   └── urls.py           # Маршруты API
├── manage.py             # Скрипт управления Django
├── PerevalDatabase.py    # Класс для работы с БД
└── pereval.sql           # Дамп базы данных (если есть)


2. Как работает API
Ваш API имеет один основной endpoint:

POST /submitData/ - для добавления новых данных о перевалах

Пример рабочего запроса (как вы уже успешно тестировали):

python
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
        "patronymic": "Иванович",
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

3. Как развернуть и запустить приложение
Установка зависимостей:

bash
pip install django djangorestframework psycopg2-binary python-dotenv requests
Настройка базы данных:

Создайте файл .env в корне проекта:

FSTR_DB_HOST=localhost
FSTR_DB_PORT=5432
FSTR_DB_LOGIN=ваш_логин
FSTR_DB_PASS=ваш_пароль
Запуск сервера:

bash
python manage.py migrate
python manage.py runserver

4. Как пользоваться API
Для мобильных разработчиков:
В мобильном приложении нужно реализовать:

Форму для ввода данных о перевале

Кнопку "Отправить", которая делает POST-запрос к вашему API

Пример кода для Android (Kotlin):

kotlin
val client = OkHttpClient()
val json = """
    {
        "beauty_title": "пер. ",
        "title": "Название перевала",
        ...
    }
""".trimIndent()

val request = Request.Builder()
    .url("http://ваш_сервер:8000/submitData/")
    .post(json.toRequestBody("application/json".toMediaType()))
    .build()

client.newCall(request).enqueue(object : Callback {
    override fun onResponse(call: Call, response: Response) {
        println("Успех: ${response.body?.string()}")
    }
    override fun onFailure(call: Call, e: IOException) {
        println("Ошибка: ${e.message}")
    }
})

Для администраторов (модераторов):
Для просмотра добавленных перевалов можно:

Использовать Django Admin (/admin)

Или добавить endpoint для GET-запросов

Чтобы добавить панель администратора:

bash
python manage.py createsuperuser

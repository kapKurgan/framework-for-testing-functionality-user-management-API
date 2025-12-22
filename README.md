# Фреймворк для автоматизированного тестирования API управления пользователями

## Цель работы

Создание автоматизированного тестового фреймворка для проверки функциональности API управления пользователями на базе PetStore Swagger API с генерацией тестовых данных, системой отчетности.

## Задачи

- Разработка базового архитектурного каркаса с реиспользуемыми компонентами
- Реализация генерации валидных и невалидных тестовых данных
- Создание покрытия CRUD-операций пользователей (создание, чтение, обновление, удаление)
- Реализация сценариев аутентификации (вход/выход)
- Подключение системы отчетности (Allure, HTML)
- Обеспечение устойчивости тестов к ошибкам и автоматической очистки данных

## Структура проекта

```bash
framework-for-testing-functionality-user-management-API/
|
|-- pytest.ini                 # Конфигурация pytest
|-- conftest.py                # Фикстуры и настройка окружения
|-- requirements.txt           # Зависимости Python
|-- Dockerfile.base            # Dockerfile для сборки контейнера
|-- docker-compose.ci.yaml     # Конфигурация Docker Compose для CI
|-- mock_petstore.py           # HTTP Mock-сервер PetStore API (создан с использованием AI)
|-- .env.example               # Пример переменных окружения
|-- .github/
|-- workflows/
|   -- api-tests.yml           # GitHub Actions workflow
|-- base/
|   -- base_test.py            # Базовый класс с HTTP-методами
|-- generators/
|   -- data_generator.py       # Генератор тестовых данных
|-- reports/
|   -- report_generator.py     # Генератор отчетов
|-- tests/
    -- test_user_api.py        # Тестовые сценарии
```

## Основные компоненты

BaseTest (base/base_test.py)

- Универсальный метод для всех HTTP-операций
- Интеграция Allure (шаги, вложения, обработка ошибок)
- Управление сессиями и таймаутами
- Валидация JSON-схем

UserDataGenerator (generators/data_generator.py)

- Генерация валидных данных пользователей
- Создание невалидных данных (пустые поля, некорректный email, длинные строки)
- Генерация тестовых данных

TestUserAPI (tests/test_user_api.py)

- 14 тестовых сценариев с маркерами
- 100% покрытие CRUD операций
- Параметризованные негативные тесты
- Проверка производительности

ReportGenerator (reports/report_generator.py)

- Генератор отчетов о тестировании

## Поддерживаемые сценарии

- Валидные данные (username, email, password, etc.)
- Пустые поля (граничное значение)
- Невалидный email-формат
- Превышение максимальной длины полей
- Пользователи с конкретным статусом

## Тестовые сценарии

```bash
---------------------------------------------------------------------------------------------------------------
| ID  | Название                               | Маркер             | Описание                                |
|-----| ---------------------------------------|--------------------|-----------------------------------------|
| 1   | test_create_user_success               | smoke, create      | Создание валидного пользователя         |
| 2   | test_create_user_with_empty_data       | regression, create | Создание пользователя с пустыми полями  |
| 3   | test_login_success                     | smoke, login       | Успешная аутентификация пользователя    |
| 4-6 | test_login_failure                     | regression, login  | Негативные сценарии входа               |
| 7   | test_logout_success                    | smoke, login       | Выход из системы                        |
| 8   | test_update_user_success               | smoke, update      | Обновление данных                       |
| 9   | test_update_nonexistent_user           | regression, update | Обновление несуществующего пользователя |
| 10  | test_delete_user_success               | smoke, delete      | Удаление пользователя                   |
| 11  | test_delete_nonexistent_user           | regression, delete | Удаление несуществующего пользователя   |
| 12  | test_get_user_success                  | smoke              | Получение данных пользователя           |
| 13  | test_get_nonexistent_user              | regression         | Получение несуществующего пользователя  |
| 14  | test_create_multiple_users_performance | performance        | Производительность                      |
---------------------------------------------------------------------------------------------------------------
```

## Как запускать тесты

Базовый запуск
```bash
pytest
```

С подробным выводом
```bash
pytest -v -s
```

Запуск по маркерам
```bash
pytest -m smoke          # Только критические тесты
pytest -m regression     # Только регрессионные тесты
pytest -m login          # Только тесты входа
```
Все маркеры указаны в разделе: Тестовые сценарии

С генерацией HTML отчета
```bash
pytest --html=reports/pytest_report.html
```

С генерацией Allure отчета
```bash
pytest --alluredir=reports/allure-results
```

Локальный просмотр Allure отчета
```bash
allure serve reports/allure-results
```

## Примечания
Если у вас возникли проблемы с запуском, попробуйте изменить пути импорта, версию pytest.
Загрузите все версии пакетов из файла requirements.txt, используйте следующую команду: 
```bash
pip install -r requirements.txt
```

## Ключевые возможности:
- HTTP Mock-сервер
- Контейнеризация Docker и Docker Compose
- Автоматический запуск тестов в GitHub Actions

Mock PetStore Server (`mock_petstore.py`)   - с использованием AI

- Эмуляция PetStore API на Flask
- Реализует все CRUD-операции пользователей: CREATE/GET/PUT/DELETE /v2/user/{username}
- Поддерживает аутентификацию: GET /v2/user/login, GET /v2/user/logout
- Хранение пользователей в оперативной памяти (имитация БД)
- Возвращает корректные HTTP-статусы и заголовки как реальный API

Доступно в интерфейсе GitHub:
Actions > API Tests > Run workflow
Можно выбрать сценарий: Фильтрация по маркерам

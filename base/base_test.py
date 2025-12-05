import requests
from typing import Dict, Any, Optional
import json


class BaseTest:
    """Базовый класс для всех тестов API"""

    BASE_URL = "https://petstore.swagger.io/v2"
    TIMEOUT = 10

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(
            self,
            method: str,
            endpoint: str,
            data=None,
            params=None,
            expected_status: int = 200
    ) -> requests.Response:
        """Универсальный метод для выполнения HTTP-запросов"""
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.request(
            method=method.upper(),
            url=url,
            json=data,
            params=params,
            timeout=self.TIMEOUT
        )
        response.raise_for_status()
        return response

    def create_user(self, user_data):
        """Создание пользователя"""
        return self._make_request("POST", "/user", data=user_data)

    def get_user(self, username):
        """Получение данных пользователя"""
        return self._make_request("GET", f"/user/{username}")

    def update_user(self, username, user_data):
        """Обновление данных пользователя"""
        return self._make_request("PUT", f"/user/{username}", data=user_data)

    def delete_user(self, username):
        """Удаление пользователя"""
        return self._make_request("DELETE", f"/user/{username}")

    def login(self, username, password):
        """Авторизация пользователя"""
        return self._make_request("GET", "/user/login", params={"username": username, "password": password})

    def logout(self):
        """Выход из системы"""
        return self._make_request("GET", "/user/logout")

    def log_response(self, response: requests.Response, test_name: str = ""):
        """Логирование ответа для отладки"""
        print(f"\n{'=' * 50}")
        print(f"ТЕСТ: {test_name}")
        print(f"URL: {response.request.url}")
        print(f"СТАТУС: {response.status_code}")
        print(f"{'=' * 50}\n")

    def validate_json_schema(self, response_data: Dict, expected_schema: Dict) -> bool:
        """Базовая валидация JSON схемы"""
        for key, value_type in expected_schema.items():
            if key not in response_data or not isinstance(response_data[key], value_type):
                return False
        return True


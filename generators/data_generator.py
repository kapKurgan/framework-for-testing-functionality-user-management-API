from faker import Faker
import random
from typing import Dict, Any, List
import json
import allure


class UserDataGenerator:
    """Генератор тестовых данных для пользователей"""

    def __init__(self, locale: str = "en_US"):
        self.fake = Faker(locale)
        self.user_statuses = [0, 1, 2, 3]

    @allure.step("Генерация данных пользователя")
    def generate_single_user(self, username: str = None) -> Dict[str, Any]:
        """Генерация данных одного пользователя"""
        user_data = {
            "id": random.randint(1000, 99999),
            "username": username or self.fake.user_name(),
            "firstName": self.fake.first_name(),
            "lastName": self.fake.last_name(),
            "email": self.fake.email(),
            "password": self.fake.password(),
            "phone": self.fake.phone_number(),
            "userStatus": random.choice(self.user_statuses)
        }
        allure.attach(
            json.dumps(user_data, indent=2, ensure_ascii=False),  # <-- Теперь json определен
            name="Сгенерированные данные",
            attachment_type=allure.attachment_type.JSON
        )
        return user_data

    @allure.step("Генерация {count} пользователей")
    def generate_bulk_users(self, count: int = 5) -> List[Dict[str, Any]]:
        """Генерация списка пользователей"""
        users = [self.generate_single_user() for _ in range(count)]
        allure.attach(
            f"Сгенерировано {len(users)} пользователей",
            name="Bulk генерация",
            attachment_type=allure.attachment_type.TEXT
        )
        return users

    @allure.step("Генерация пользователя со статусом {status}")
    def generate_user_with_specific_status(self, status: int) -> Dict[str, Any]:
        """Генерация пользователя с конкретным статусом"""
        user = self.generate_single_user()
        user["userStatus"] = status
        return user

    @allure.step("Генерация невалидных данных: {invalid_type}")
    def generate_invalid_user_data(self, invalid_type: str = "missing_required") -> Dict[str, Any]:
        """Генерация невалидных данных для негативных тестов"""
        if invalid_type == "missing_required":
            return {"userStatus": 1}

        elif invalid_type == "invalid_email":
            user = self.generate_single_user()
            user["email"] = "not-an-email"
            return user

        elif invalid_type == "empty_fields":
            return {
                "id": 0, "username": "", "firstName": "", "lastName": "",
                "email": "", "password": "", "phone": "", "userStatus": 0
            }

        elif invalid_type == "long_strings":
            user = self.generate_single_user()
            user["username"] = "a" * 1000
            user["firstName"] = "b" * 1000
            return user

        else:
            return {"invalid": "data"}







import allure
import pytest
import requests
from data import BASE_URL, ERROR_USER_EXISTS, ERROR_MISSING_FIELDS
from helpers.user_helpers import register_user, generate_unique_user_data

@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Создание уникального пользователя (через фикстуру)")
    def test_create_unique_user_with_fixture(self, new_user):
        assert new_user["email"] is not None
        assert new_user["password"] is not None
        assert new_user["name"] is not None

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, new_user):
        payload = {
            "email": new_user["email"],
            "password": new_user["password"],
            "name": new_user["name"]
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)
        assert response.status_code == 403
        assert response.json().get("message") == ERROR_USER_EXISTS

    @allure.title("Создание пользователя без одного из обязательных полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        user_data = generate_unique_user_data()
        del user_data[missing_field]
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        assert response.status_code == 403
        assert response.json().get("message") == ERROR_MISSING_FIELDS
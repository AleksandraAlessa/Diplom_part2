import allure
import pytest
import requests
from data import BASE_URL, ERROR_INVALID_CREDENTIALS


@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user(self, base_url, new_user):
        # Фикстура создала пользователя, используем его данные
        response = requests.post(
            f"{base_url}/api/auth/login",
            json={"email": new_user["email"], "password": new_user["password"]}
        )
        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "accessToken" in response.json()
        assert response.json()["user"]["email"] == new_user["email"]
        assert response.json()["user"]["name"] == new_user["name"]

    @allure.title("Вход с неверным логином")
    def test_login_wrong_email(self, base_url, new_user):
        payload = {"email": "wrong@test.ru", "password": new_user["password"]}
        response = requests.post(f"{base_url}/api/auth/login", json=payload)
        assert response.status_code == 401
        assert response.json().get("message") == ERROR_INVALID_CREDENTIALS

    @allure.title("Вход с неверным паролем")
    def test_login_wrong_password(self, base_url, new_user):
        payload = {"email": new_user["email"], "password": "wrong_password"}
        response = requests.post(f"{base_url}/api/auth/login", json=payload)
        assert response.status_code == 401
        assert response.json().get("message") == ERROR_INVALID_CREDENTIALS

    @allure.title("Вход с неверными логином и паролем")
    def test_login_wrong_both(self, base_url):
        payload = {"email": "wrong@test.ru", "password": "wrong_password"}
        response = requests.post(f"{base_url}/api/auth/login", json=payload)
        assert response.status_code == 401
        assert response.json().get("message") == ERROR_INVALID_CREDENTIALS
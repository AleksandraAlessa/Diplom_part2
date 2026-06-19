import allure
import pytest
import requests
from data import BASE_URL, INVALID_INGREDIENT_ID, ERROR_NO_INGREDIENTS

@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, base_url, auth_headers, ingredient_ids):
        ingredients = ingredient_ids[:2] if len(ingredient_ids) >= 2 else ingredient_ids
        payload = {"ingredients": ingredients}
        response = requests.post(f"{base_url}/api/orders", json=payload, headers=auth_headers)
        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "order" in response.json()
        assert "number" in response.json()["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, base_url, ingredient_ids):
        ingredients = ingredient_ids[:2] if len(ingredient_ids) >= 2 else ingredient_ids
        payload = {"ingredients": ingredients}
        response = requests.post(f"{base_url}/api/orders", json=payload)
        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "order" in response.json()
        assert "number" in response.json()["order"]

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, base_url, auth_headers, ingredient_ids):
        payload = {"ingredients": ingredient_ids}
        response = requests.post(f"{base_url}/api/orders", json=payload, headers=auth_headers)
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, base_url, auth_headers):
        payload = {"ingredients": []}
        response = requests.post(f"{base_url}/api/orders", json=payload, headers=auth_headers)
        assert response.status_code == 400
        assert response.json().get("message") == ERROR_NO_INGREDIENTS

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_invalid_ingredient_hash(self, base_url, auth_headers):
        payload = {"ingredients": [INVALID_INGREDIENT_ID]}
        response = requests.post(f"{base_url}/api/orders", json=payload, headers=auth_headers)
        assert response.status_code == 500
import pytest
import requests
from data import BASE_URL, VALID_INGREDIENT_IDS
from helpers.user_helpers import register_user, delete_user

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def ingredient_ids():
    """
    Получает реальные ID ингредиентов из API.
    Если запрос не удаётся, возвращает запасные ID из data.py.
    """
    try:
        response = requests.get(f"{BASE_URL}/api/ingredients")
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "data" in data:
                ids = [item["_id"] for item in data["data"]]
                if ids:
                    return ids
    except Exception:
        pass
    # Fallback: используем ID из документации
    return VALID_INGREDIENT_IDS

@pytest.fixture(scope="function")
def new_user():
    """Создаёт нового пользователя и возвращаетданные и токкен, после теста удаляет."""
    response, user_data = register_user()
    assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"
    
    # Получаем accessToken после успешной регистрации
    token = response.json().get("accessToken", "")
    access_token = token.replace("Bearer ", "") if token else None
    
    yield {
        "email": user_data["email"],
        "password": user_data["password"],
        "name": user_data["name"],
        "access_token": access_token
    }
    
     # Удаление пользователя после теста
    if access_token:
        delete_response = delete_user(access_token)

@pytest.fixture
def auth_headers(new_user):
    """Возвращает заголовки с авторизацией для авторизованных запросов."""
    token = new_user["access_token"]
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


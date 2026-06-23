import pytest
import requests
from data import BASE_URL, VALID_INGREDIENT_IDS
from helpers.user_helpers import register_user, delete_user

@pytest.fixture(scope="session")
def ingredient_ids():
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
    return VALID_INGREDIENT_IDS

@pytest.fixture(scope="function")
def new_user():
    response, user_data = register_user()
    assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"
    token = response.json().get("accessToken", "")
    access_token = token.replace("Bearer ", "") if token else None
    yield {
        "email": user_data["email"],
        "password": user_data["password"],
        "name": user_data["name"],
        "access_token": access_token
    }
    if access_token:
        delete_user(access_token)

@pytest.fixture
def auth_headers(new_user):
    token = new_user["access_token"]
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

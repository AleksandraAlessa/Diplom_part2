import random
import string
import requests
from data import BASE_URL

def generate_random_string(length=10):
    """Генерирует случайную строку из букв и цифр."""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_unique_user_data():
    """Генерирует уникальные данные для пользователя."""
    return {
        "email": f"{generate_random_string(8)}@test.ru",
        "password": generate_random_string(8),
        "name": generate_random_string(8)
    }

def register_user(email=None, password=None, name=None):
    """
    Регистрирует пользователя и возвращает ответ и данные.
    Если поля не переданы — генерирует уникальные.
    """
    if email is None or password is None or name is None:
        user_data = generate_unique_user_data()
        email = user_data["email"]
        password = user_data["password"]
        name = user_data["name"]
    
    payload = {"email": email, "password": password, "name": name}
    response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)
    return response, {"email": email, "password": password, "name": name}

def login_user(email, password):
    """Авторизует пользователя и возвращает ответ."""
    payload = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=payload)
    return response

def get_access_token(response):
    """Извлекает accessToken из ответа авторизации."""
    if response.status_code == 200:
        token = response.json().get("accessToken", "")
        return token.replace("Bearer ", "") if token else None
    return None

def delete_user(access_token):
    """Удаляет пользователя по токену."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(f"{BASE_URL}/api/auth/user", headers=headers)
    return response
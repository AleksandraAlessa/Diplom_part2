import random
import string

BASE_URL = "https://stellarburgers.education-services.ru"

# Сообщения об ошибках из документации
ERROR_USER_EXISTS = "User already exists"
ERROR_MISSING_FIELDS = "Email, password and name are required fields"
ERROR_INVALID_CREDENTIALS = "email or password are incorrect"
ERROR_UNAUTHORIZED = "You should be authorised"
ERROR_NO_INGREDIENTS = "Ingredient ids must be provided"

# Валидные хеши ингредиентов (если не ответит GET /api/ingredients)
VALID_INGREDIENT_IDS = [
    "60d3b41abdacab0026a733c6",
    "609646e4dc916e00276b2870"
]
INVALID_INGREDIENT_ID = "invalid_hash_123"
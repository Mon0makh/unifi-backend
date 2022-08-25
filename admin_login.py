import hashlib
import random
import string
from datetime import datetime, timedelta

from connect_db import get_admin_login, get_admin_by_token, save_admin_token

# from app.models.database import database
# from app.models.users import tokens_table, users_table
# from app.schemas import users as user_schema

def get_random_string(length=12):
    """ Генерирует случайную строку, использующуюся как соль """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """ Хеширует пароль с солью """
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """ Проверяет, что хеш пароля совпадает с хешем из БД """
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_user_by_login(login: str):
    """ Возвращает информацию о пользователе """
    return await get_admin_login(login)


async def get_user_by_token(token: str):
    """ Возвращает информацию о владельце указанного токена """
    return await get_admin_by_token(token)


async def create_user_token(login: str):
    """ Создает токен для пользователя с указанным user_id """
    token = " "
    expires = datetime.now() + timedelta(weeks=2)
    save_admin_token(login, token, expires)

    # query = (
    #     tokens_table.insert()
    #     .values(expires=datetime.now() + timedelta(weeks=2), user_id=user_id)
    #     .returning(tokens_table.c.token, tokens_table.c.expires)
    # )

    return token, expires


# async def create_user(user: user_schema.UserCreate):
#     """ Создает нового пользователя в БД """
#     salt = get_random_string()
#     hashed_password = hash_password(user.password, salt)
#     query = users_table.insert().values(
#         email=user.email, name=user.name, hashed_password=f"{salt}${hashed_password}"
#     )
#     user_id = await database.execute(query)
#     token = await create_user_token(user_id)
#     token_dict = {"token": token["token"], "expires": token["expires"]}
#
#     return {**user.dict(), "id": user_id, "is_active": True, "token": token_dict}
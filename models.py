from datetime import datetime

from pydantic import BaseModel, ValidationError, UUID4, Field, validator
from pydantic.color import Color

from typing import List, Union, Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str

class LoginFormSettings(BaseModel):
    langs: List[str]
    count_langs: int
    count_fields: int
    api_url: str


class TextLangs(BaseModel):
    lang: str
    text: str


class GuestFields(BaseModel):
    type: str
    title: str
    description: Union[str, None]
    brand_icon: Union[str, None]


class GuestLogin(BaseModel):
    count_lang: int
    fields: List[GuestFields]


class LoginFormField(BaseModel):
    field_type: str
    api_name: Union[str, None]
    field_title: List[TextLangs]
    description: Union[List[TextLangs], None]
    brand_icon: Union[str, None]


class LoginFormFields(BaseModel):
    fields: List[LoginFormField]


class LoginForm(BaseModel):
    login: str  # session_key
    settings: LoginFormSettings
    fields: List[LoginFormField]

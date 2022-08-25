from datetime import datetime

from pydantic import BaseModel, ValidationError, UUID4, Field, validator
from pydantic.color import Color

from typing import List, Union, Optional


class UserCreate(BaseModel):
    name: str
    password: str


class UserBase(BaseModel):
    """ Формирует тело ответа с деталями пользователя """
    id: int
    name: str


class TokenBase(BaseModel):
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def hexlify_token(cls, value):
        """ Конвертирует UUID в hex строку """
        return value.hex


class User(UserBase):
    """ Формирует тело ответа с деталями пользователя и токеном """
    token: TokenBase = {}


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
    langs: List[str]
    count_langs: int
    fields: List[GuestFields]


class LoginFormField(BaseModel):
    number: int
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

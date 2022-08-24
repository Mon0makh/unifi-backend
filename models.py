from pydantic import BaseModel, ValidationError
from pydantic.color import Color

from typing import List, Union


class LoginFormSettings(BaseModel):
    langs: List[str]
    count_langs: int
    count_fields: int
    api_url: str


class BrandIcon(BaseModel):
    brands_img: str
    brands_api_name: str


class TextLangs(BaseModel):
    lang: str
    text: str


class GuestFields(BaseModel):
    type: str
    title: str
    description: Union[str, None]
    brands: Union[BrandIcon, None]


class GuestLogin(BaseModel):
    lang: str
    fields: List[GuestFields]


class LoginFormField(BaseModel):
    number: int
    field_type: str
    api_name: Union[str, None]
    field_title: List[TextLangs]
    description: Union[List[TextLangs], None]
    brands: Union[BrandIcon, None]


class LoginFormFields(BaseModel):
    fields: List[LoginFormField]


class LoginForm(BaseModel):
    login: str  # session_key
    settings: LoginFormSettings
    fields: List[LoginFormField]

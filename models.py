from pydantic import BaseModel, ValidationError
from pydantic.color import Color

from typing import List, Union


class LoginFormSettings(BaseModel):
    langs: List[str]
    count_langs: int
    logo_img: str
    bg_img: Union[str, None]
    bg_color: Union[Color, None]
    count_fields: int


class BrandIcon(BaseModel):
    brands_img: str
    brands_api_name: str

class text_langs:
    lang: str
    text: str

class LoginFormField(BaseModel):
    number: int
    field_type: str
    api_name: Union[str, None]
    field_title: List[text_langs]
    description: Union[List[text_langs], None]
    brands: Union[BrandIcon, None]


class LoginFormFields(BaseModel):
    fields: List[LoginFormField]


class LoginForm(BaseModel):
    login: str  # session_key
    settings: LoginFormSettings
    fields: List[LoginFormField]

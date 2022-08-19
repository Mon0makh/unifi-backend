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


class LoginFormField(BaseModel):
    number: int
    field_type: str
    api_name: Union[str, None]
    field_title: List[str]
    description: Union[List[str], None]
    brands_img: Union[List[str], None]
    brands_api_name: Union[List[str], None]


class LoginFormFields(BaseModel):
    fields: List[LoginFormField]


class LoginForm(BaseModel):
    login: str  # session_key
    settings: LoginFormSettings
    fields: List[LoginFormField]

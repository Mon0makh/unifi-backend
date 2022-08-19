from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
from pydantic.color import Color

from models import LoginForm, LoginFormFields


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/LoginForm/")
async def create_item(item: LoginForm):
    return item

@app.post("/FormFields/")
async def create_item(item: LoginFormFields):
    return item
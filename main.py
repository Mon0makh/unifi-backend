from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
from pydantic.color import Color

from models import LoginForm


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: str, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/LoginForm/")
async def create_item(item: LoginForm):
    return item

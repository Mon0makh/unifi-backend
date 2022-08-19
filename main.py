from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


from models import LoginForm, LoginFormFields

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/LoginForm/")
async def create_item(item: LoginForm):
    return item


@app.post("/FormFields/")
async def create_item(item: LoginFormFields):
    return item

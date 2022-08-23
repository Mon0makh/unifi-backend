from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from models import LoginForm, LoginFormFields

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://185.125.88.30:8000",
    "https://freewifi.ws-gropup.kz/api"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
async def login_form_post(item: LoginForm):
    if len(item.settings.langs) != item.settings.count_langs:
        raise HTTPException(status_code=400, detail="ОШИБКА! Количество языков не совпадает!")

    if len(item.fields) != item.config.count_fields:
        raise HTTPException(status_code=400, detail="ОШИБКА! Количество полей не совпадает!")

    for field in item.fields:
        if len(field.field_title) != len(item.settings.langs):
            raise HTTPException(status_code=400, detail="ОШИБКА! Пустое название поля: " + str(field.number))
        if field.description is not None:
            if len(field.description) != len(item.settings.langs):
                raise HTTPException(status_code=400, detail="ОШИБКА! Пустое описание поля: " + str(field.number))

    print(item)
    return item


@app.post("/FormFields/")
async def test_form_fields(item: LoginFormFields):
    return item

# {
#   "login": "string",
#   "settings": {
#     "langs": [
#       "string"
#     ],
#     "count_langs": 0,
#     "logo_img": "string",
#     "bg_img": "string",
#     "bg_color": "string",
#     "count_fields": 0
#   },
#   "fields": [
#     {
#       "number": 0,
#       "field_type": "string",
#       "api_name": "string",
#       "field_title": [
#         "string"
#       ],
#       "description": [
#         "string"
#       ],
#       "brands": {
#         "brands_img": "string",
#         "brands_api_name": "string"
#       }
#     }
#   ]
# }

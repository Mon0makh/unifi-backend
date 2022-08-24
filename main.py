from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.requests import Request
from fastapi.responses import Response
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware



from models import LoginForm, LoginFormFields
from data_verification import login_form_data_verification
from connect_db import get_guest_login_form, get_lang_list_from_db
app = FastAPI()

ALLOWED_ORIGINS = "*"

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# handle CORS preflight requests
@app.options('/{rest_of_path:path}')
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    return response


# set CORS headers
@app.middleware("http")
async def add_CORS_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/")
def read_root():
    return Response(content="Server OK", status_code=200)


# TODO функция аутентификации
@app.post("/LoginForm/")
async def login_form_post(item: LoginForm):
    code, response_text = login_form_data_verification(item)
    return Response(content=response_text, status_code=code)


## Временное
@app.post("/FormFields/")
async def test_form_fields(item: LoginFormFields):
    return item


@app.get("/GetLangsList/")
def get_lang_list():
    langs = get_lang_list_from_db()
    return langs


@app.get("/GetLoginFormFields/")
def get_login_form_fields():
    form = get_guest_login_form("rus")
    return form


@app.post("/AdminAuth/")
async def admin_auth():
    return {}


@app.post("/GuestAuth/")
async def guest_auth():
    return {}

@app.post("/UploadBGImage/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

@app.post("/UploadLogoImage/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
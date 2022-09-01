from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, status, Header, Form
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import sys, os


from models import LoginForm, LoginFormFields, GuestLogin, GuestFields, Token, User
from data_verification import login_form_data_verification
from connect_db import get_guest_login_form, get_lang_list_from_db, get_guest_login_form_to_admin
from send_data import send_guest_data


from admin_auth import login_for_access_token, get_current_active_user

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


@app.post("/AdministratorSignIn", response_model=Token)
async def login_admin(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login_for_access_token(form_data)


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.post("/LoginForm/")
async def login_form_post(item: LoginForm, current_user: User = Depends(get_current_active_user)):
    code, response_text = login_form_data_verification(item)
    return Response(content=response_text, status_code=code)


@app.get("/GetAdminLoginForm/")
async def login_form_post(current_user: User = Depends(get_current_active_user)):
    return get_guest_login_form_to_admin()


@app.get("/GetAllLangsList/")
def get_lang_list():
    langs = get_lang_list_from_db()
    return langs


@app.get("/GetLoginForm/{lang}")
async def get_login_form_fields(lang: str):
    form = get_guest_login_form(lang)
    return form


@app.post("/GuestAuth/")
async def guest_auth(form: GuestLogin):
    request = send_guest_data(form)
    return request


@app.post("/UploadBGImage/")
async def create_upload_file(
        file: bytes = File(),
        img_type: str = Form(),
        current_user: User = Depends(get_current_active_user)
    ):
    if file is None:
        return {"message": "No upload file sent"}
    else:
        with open('/var/www/html/img/imageBG.' + img_type, 'wb') as image:
            image.write(file)
            image.close()
        return Response(content="imageBG", status_code=200)


@app.post("/UploadLogoImage/")
async def create_file(
        file: bytes = File(),
        img_type: str = Form(),
        current_user: User = Depends(get_current_active_user)
    ):
    if file is None:
        return {"message": "No upload file sent"}
    else:

        with open('/var/www/html/img/imageLogo.'+img_type, 'wb') as image:
            image.write(file)
            image.close()
        return Response(content="imageLogo", status_code=200)


@app.post("/UploadBrandImage/")
async def create_file(
        file: bytes = File(),
        img_type: str = Form(),
        number: int = Form(),
        current_user: User = Depends(get_current_active_user)
    ):
    if file is None:
        return {"message": "No upload file sent"}
    else:
        with open('/var/www/html/img/imageBrand'+str(number)+'.' + img_type, 'wb') as image:
            image.write(file)
            image.close()

        return Response(content='imageBrand'+str(number)+'.' + img_type, status_code=200)

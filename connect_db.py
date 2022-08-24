from pymongo import MongoClient

from config import MONGODB_LINK
from config import MONGO_DB

from models import LoginForm, LoginFormFields, LoginFormSettings

# Connect to DataBase
mondb = MongoClient(MONGODB_LINK)[MONGO_DB]


def get_lang_list_from_db():
    langs = mondb.langs_list.find({})
    # try:
    #
    # except:
    #     return 0
    return langs


def get_guest_login_form(lang: str):
    form = mondb.login_fields.find_one({'_key': 0})

    return form


def save_guest_login_form(fields: LoginForm):
    mondb.login_fields.update_one(
        {'_key': 0},
        {'$set':
             {'login': fields.login,
              'settings': {
                  'langs': fields.settings.langs,
                  'count_langs': fields.settings.langs,
                  'logo_img': fields.settings.logo_img,
                  'bg_img': fields.settings.bg_img,
                  'count_fields': fields.settings.count_fields,
                  'api_url': fields.settings.api_url},
              }
         }
    )
    return False

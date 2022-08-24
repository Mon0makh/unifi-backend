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
             {'form': fields}
         }
    )
    return False

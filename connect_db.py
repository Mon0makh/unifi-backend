from pymongo import MongoClient
from datetime import datetime, timedelta
from config import MONGODB_LINK
from config import MONGO_DB

from models import LoginForm, LoginFormFields, LoginFormSettings

# Connect to DataBase
mondb = MongoClient(MONGODB_LINK)[MONGO_DB]


def get_lang_list_from_db():
    langs_db = mondb.langs_list.find({})
    langs = {lang['lang'] for lang in langs_db}

    # try:
    #
    # except:
    #     return 0

    return langs


def get_lang_list_form():
    form_db = mondb.login_form.find_one({'_key': 0})
    langs_db = form_db['settings']['langs'],
    langs = {lang for lang in langs_db}

    # try:
    #
    # except:
    #     return 0

    return langs


def get_guest_login_form(lang: str):
    form_db = mondb.login_form.find_one({'_key': 0})

    form = {
        'langs': form_db['settings']['langs'],
        'fields': [],
        'count_langs': form_db['settings']['count_langs'],
        'count_fields': form_db['settings']['count_fields']
    }

    for field in form_db['fields']:
        field_g = {
            'type': field['type'],
            'title': field['title'][lang],
            'description': field.get('description').get(lang),
            'brands': field.get('brands')
        }
        form['fields'].append(field_g)
    return form


def get_admin_login(login: str):
    user_db = mondb.admins.find_one({'login': login})
    if user_db is not None:
        user = {login: {
            "username": user_db.username,
            "full_name": user_db.full_name,
            "email": user_db.email,
            "hashed_password": user_db.hashed_password,
            "disable": user_db.disable
        }}
        return user

    else:
        return None


def save_admin_user():
    pass


def get_guest_login_form_to_admin():
    form_db = mondb.login_fom.find_one({'_key': 0})
    form = {'settings': {
        'login': form_db.login,
        'langs': form_db.settings.langs,
        'count_langs': form_db.settings.count_langs,
        'count_fields': form_db.settings.count_fields,
        'api_url': form_db.settings.api_url
    },
        'fields': []
    }

    for field in form_db.fields:
        field_g = {'type': field.field_type, 'brand_icon': field.brand_icon, 'title': {}, 'description': {}}

        for lang_index in range(form_db.settings.count_langs):
            field_g['title'][field.field_title[lang_index].lang] = field.field_title[lang_index].text
            field_g['description'][field.description[lang_index].lang] = field.description[lang_index].text

        form['fields'].append(field_g)

    return form


def save_guest_login_form(fields: LoginForm):
    form = {'settings': {
        'login': fields.login,
        'langs': fields.settings.langs,
        'count_langs': fields.settings.count_langs,
        'count_fields': fields.settings.count_fields,
        'api_url': fields.settings.api_url
    },
        'fields': []
    }

    for field in fields.fields:
        field_g = {'type': field.field_type, 'brand_icon': field.brand_icon, 'title': {}, 'description': {}}

        for lang_index in range(fields.settings.count_langs):
            field_g['title'][field.field_title[lang_index].lang] = field.field_title[lang_index].text
            if field.description[lang_index].lang is not None:
                field_g['description'][field.description[lang_index].lang] = field.description[lang_index].text

        form['fields'].append(field_g)

    mondb.login_form.update_one(
        {'_key': 0},
        {'$set': form}
    )
    return False

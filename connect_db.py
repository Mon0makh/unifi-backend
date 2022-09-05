from pymongo import MongoClient
from datetime import datetime

from config import MONGODB_LINK, MONGO_DB
from models import LoginForm, GuestLogin
from admin_auth import verify_password, get_password_hash

# Connect to DataBase
mondb = MongoClient(MONGODB_LINK)[MONGO_DB]


def get_lang_list_from_db():
    # try:
    #     langs_db = mondb.lang_list.find({})
    # except:
    #     # TODO LOGING
    #     return []
    # langs = []
    # for i in range(4, -1, -1):
    #     for lang in langs_db:
    #         if lang['number'] == i:
    #             langs.append(lang['lang'])
    langs = ['rus', 'eng', 'kaz', 'tur', 'ita']
    # langs = {lang['lang'] for lang in langs_db}
    return langs


def get_guest_login_form(lang: str):
    try:
        form_db = mondb.login_form.find_one({'_key': 0})
    except:
        # TODO LOGING
        return None
    if len(form_db) > 2:
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
                'api_name': field['api_name'],
                'description': field.get('description').get(lang),
                'brand_icon': field.get('brand_icon')
            }
            form['fields'].append(field_g)
        return form
    else:
        return None


def get_admin_login(login: str):
    try:
        user_db = mondb.admins.find_one({'username': login})
    except:
        # TODO LOGGING
        return None

    if user_db is not None:
        user = {
            "username": user_db['username'],
            "full_name": user_db['full_name'],
            "email": user_db['email'],
            "hashed_password": user_db['hashed_password'],
            "disabled": user_db['disabled']
        }
        return user

    else:
        return None


def get_url():
    try:
        url = mondb.login_form.find_one({'_key': 0})['settings']['api_url']
        return url
    except:
        # TODO
        return ""


def save_admin_user():
    pass  # TODO


def get_guest_login_form_to_admin():
    try:
        form_db = mondb.login_form.find_one({'_key': 0})
        if form_db is None:
            raise Exception('NO FORM in database!')
    except:
        return {}

    if len(form_db) > 2:
        form = {'settings': {
            'login': form_db['settings']['login'],
            'langs': form_db['settings']['langs'],
            'count_langs': form_db['settings']['count_langs'],
            'count_fields': form_db['settings']['count_fields'],
            'api_url': form_db['settings']['api_url']
        },
            'fields': []
        }

        for field in form_db['fields']:
            field_g = {'type': field['type'], 'brand_icon': field['brand_icon'], 'api_name': field['api_name'],
                       'title': {}, 'description': {}, 'api_value': field['api_value']}

            for lang in form_db['settings']['langs']:
                field_g['title'][lang] = field['title'][lang]
                if len(field.get('description')) > 0:
                    field_g['description'][lang] = field['description'][lang]

            form['fields'].append(field_g)

        return form
    else:
        return None


def save_guest_login_form(fields: LoginForm):
    try:
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
            field_g = {'type': field.field_type, 'brand_icon': field.brand_icon, 'api_name': field.api_name,
                       'title': {}, 'description': {}, 'api_value': field.api_value}

            for lang_index in range(fields.settings.count_langs):
                field_g['title'][field.field_title[lang_index].lang] = field.field_title[lang_index].text
                if field.description is not None:
                    field_g['description'][field.description[lang_index].lang] = field.description[lang_index].text

            form['fields'].append(field_g)

        mondb.login_form.update_one(
            {'_key': 0},
            {'$set': form}
        )

    except:
        return True

    return False


def save_guest_data(data: GuestLogin):
    try:
        form = {'lang': data.lang,
                'fields': []
                }

        for field in data.fields:
            if field.type == "front":
                continue
            field_g = {'time': datetime.now().strftime("%Y.%m.%d %H:%M:%S"), 'type': field.type,
                       'title': field.title, 'api_name': field.api_name, 'value': field.value}

            form['fields'].append(field_g)

        mondb.guests_data.insert_one(form)
        return False

    except:
        return True


def save_new_admin_password(username: str, old_password: str, new_pass: str):
    try:
        user = mondb.admins.find_one({'username': username})
        if user is not None:
            if verify_password(old_password, user['hashed_password']):
                mondb.admins.update_one({'_id': user['_id']}, {'$set': {'hashed_password': get_password_hash(new_pass)}})
                return False
            else:
                return "Password Incorrect!"
        return "User doesnt exist"
    except:
        return "Error connect to db!"

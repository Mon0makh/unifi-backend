from pymongo import MongoClient
from datetime import datetime

from config import MONGODB_LINK, MONGO_DB
from models import LoginForm, GuestLogin

# Connect to DataBase
mondb = MongoClient(MONGODB_LINK)[MONGO_DB]


def get_lang_list_from_db():
    langs = ['ru_RU', 'en_EN', 'kk_KZ', 'tr_TR', 'it_IT']
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
            'langs_flags': [],
            'fields': [],
            'count_langs': form_db['settings']['count_langs'],
            'count_fields': form_db['settings']['count_fields'],
            'bg_image': form_db['settings']['bg_image'],
            'logo_image': form_db['settings']['logo_image']
        }

        ## ВРЕМЕННОЕ ПЕРЕДЕЛАТЬ
        for _lang in form['langs']:
            if _lang == 'ru_RU':
                form['langs_flags'].append('🇷🇺')
            elif _lang == 'en_EN':
                form['langs_flags'].append('🇺🇸')
            elif _lang == 'kk_KZ':
                form['langs_flags'].append('🇰🇿')
            elif _lang == 'tr_TR':
                form['langs_flags'].append('🇹🇷')
            elif _lang == 'it_IT':
                form['langs_flags'].append('🇮🇹')

        ## ВРЕМЕННОЕ ПЕРЕДЕЛАТЬ
        if lang == 'ru_RU':
            form['submit_lang'] = 'Отправить'
        elif lang == 'en_En':
            form['submit_lang'] = 'Send'
        elif lang == 'kk_KZ':
            form['submit_lang'] = 'Жіберу'
        elif lang == 'tr_TR':
            form['submit_lang'] = 'Göndermek'
        elif lang == 'it_IT':
            form['submit_lang'] = 'Inviare'

        for field in form_db['fields']:
            field_g = {
                'type': field['type'],
                'title': field['title'][lang],
                'api_name': field['api_name'],
                'description': field.get('description').get(lang),
                'brand_icon': field.get('brand_icon'),
                'api_value': field.get('api_value'),
                'required_field': field.get('required_field')
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
            'api_url': form_db['settings']['api_url'],
            'bg_image': form_db['settings']['bg_image'],
            'logo_image': form_db['settings']['logo_image']
        },
            'fields': []
        }

        for field in form_db['fields']:
            field_g = {'type': field['type'], 'brand_icon': field.get('brand_icon'), 'api_name': field['api_name'],
                       'title': {}, 'description': {},
                       'api_value': None if field.get('api_value') is None else field.get('api_value'),
                       'required_field': field.get('required_field')}

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

        if fields.settings.bg_image is not None:
            form['settings']['bg_image'] = fields.settings.bg_image
        if fields.settings.logo_image is not None:
            form['settings']['logo_image'] = fields.settings.logo_image

        for field in fields.fields:
            field_g = {'type': field.field_type, 'brand_icon': field.brand_icon, 'api_name': field.api_name,
                       'title': {}, 'description': {}, 'api_value': field.api_value,
                       'required_field': field.required_field}

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


def save_new_admin_password(username: str, new_pass: str):
    try:
        mondb.admins.update_one({'username': username}, {'$set': {'hashed_password': new_pass}})
        return False
    except:
        return "Error connect to db!"

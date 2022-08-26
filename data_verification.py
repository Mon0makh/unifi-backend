from models import LoginForm, LoginFormFields
from connect_db import save_guest_login_form


def login_form_data_verification(item: LoginForm):
    if len(item.settings.langs) != item.settings.count_langs:
        return 400, "ОШИБКА! Количество языков не совпадает!"

    if len(item.fields) != item.settings.count_fields:
        return 400, "ОШИБКА! Количество полей не совпадает!"

    for field in item.fields:
        if len(field.field_title) != len(item.settings.langs):
            return 400, "ОШИБКА! Пустое название поля"
        if field.description is not None:
            if len(field.description) != len(item.settings.langs):
                return 400, "ОШИБКА! Пустое описание поля"

    if save_guest_login_form(item):
        return 500, "ОШИБКА! Не удалось сохранить данные на сервере! Возможно база данных не доступна!"

    return 200, "Данные успешно приняты!"

from models import LoginForm, LoginFormFields
from connect_db import save_guest_login_form


def login_form_data_verification(item: LoginForm):
    if len(item.settings.langs) != item.settings.count_langs:
        return 400, "ERROR! Number of languages does not match!"

    if len(item.fields) != item.settings.count_fields:
        return 400, "Error! Number of fields does not match!"

    for field_numb in range(len(item.fields)):
        if len(item.fields[field_numb].field_title) != item.settings.count_langs:

            return 400, "Error! Empty field title: " + str(field_numb)
        if item.fields[field_numb].description is not None:
            if len(item.fields[field_numb].description) != len(item.settings.langs):
                return 400, "Error! Empty description: " + str(field_numb)

    if save_guest_login_form(item):
        return 500, "Error! Cannot load data to server! DataBase may be offline!"

    return 200, "Data loaded successfully!"

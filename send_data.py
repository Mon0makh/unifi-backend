import requests

from connect_db import get_url, save_guest_data
from models import GuestLogin


def send_guest_data(data: GuestLogin):
    url = get_url()
    query_params = {'FIELDS[TITLE]': '. WiFi'}

    db_save = save_guest_data(data)
    if db_save:
        return 500, "Error! Cannot load data to server! DataBase may be offline!"

    client_name = ""

    brands_index = 0
    for field in data.fields:
        if field.type == 'brand' and field.value is not None:
            query_params['FIELDS[UF_CRM_1537246407][' + str(brands_index) + ']'] = field.value
            brands_index += 1

        if field.type == 'textfield':
            if field.api_name == 'FIELD[NAME]':
                client_name = client_name + field.value
            if field.api_name == 'FIELD[LAST_NAME]':
                client_name = client_name + field.value
                
            query_params[field.api_name] = field.value

        else:
            query_params[field.api_name] = field.value

    query_params['FIELDS[SOURCE_ID]'] = 'UC_QJSB1V'
    query_params['FIELDS[TITLE]'] = client_name + (query_params['FIELDS[TITLE]']) if len(client_name) > 2 else "Гость" + (query_params['FIELDS[TITLE]'])
    try:
        response = requests.get(url, params=query_params)
        return 200, "SUCCESS!"
    except:
        return 500, "Error! Cannot load data to API Server!"

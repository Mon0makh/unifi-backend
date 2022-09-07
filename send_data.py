import requests

from connect_db import get_url, save_guest_data
from models import GuestLogin


def send_guest_data(data: GuestLogin):
    url = get_url()
    query_params = {'FIELDS[TITLE]': 'ТЕСТ. Из WiFi'}

    db_save = save_guest_data(data)
    if db_save:
        return 500, "Error! Cannot load data to server! DataBase may be offline!"

    brands_index = 0
    for field in data.fields:
        if field.type == 'brand' and field.value is not None:
            query_params['FIELDS[UF_CRM_1537246407][' + str(brands_index) + ']'] = field.value
            brands_index += 1
        elif field.type == 'button':
            continue
        else:
            query_params[field.api_name] = field.value

    query_params['FIELDS[SOURCE_ID]'] = 'UC_QJSB1V'

    try:
        response = requests.get(url, params=query_params)
        return 200, "SUCCESS!"
    except:
        return 500, "Error! Cannot load data to API Server!"

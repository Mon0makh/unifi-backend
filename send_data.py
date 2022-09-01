import requests

from connect_db import get_url, save_guest_data
from models import GuestLogin

def send_guest_data(data: GuestLogin):
    url = get_url()
    myobj = {'somekey': 'somevalue'}

    db_save = save_guest_data(data)
    if db_save:
        return 500, "Error! Cannot load data to server! DataBase may be offline!"



    x = requests.get(url, json=myobj)
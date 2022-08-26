import requests

from connect_db import get_url
from models import GuestLogin
def send_guest_data(data: GuestLogin):
    url = get_url()
    myobj = {'somekey': 'somevalue'}

    x = requests.post(url, json=myobj)
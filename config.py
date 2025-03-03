# langs setting
ALL_LANGS = ['ru_RU', 'en_EN', 'kk_KZ', 'tr_TR', 'it_IT']

SEND_TEXT = {'ru_RU': 'Подключиться',
             'en_EN': 'Connect',
             'kk_KZ': 'Қосылу',
             'tr_TR': 'Bağlamak',
             'it_IT': 'Collegare'}


# DB Connect
MONGODB_LINK = "mongodb://127.0.0.1:27017/?retryWrites=true&w=majority"
MONGO_DB = "unifi"

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

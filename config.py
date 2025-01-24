import os

class Config:
    API_KEY = os.getenv("IMEI_API")
    TG_TOKEN = ''
    BASE_URL = 'https://api.imeicheck.net'
    FULL_URL = BASE_URL + '/v1/checks'
    SERVICE_ID = 12
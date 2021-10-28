import requests
import json

def pushNotification(content):
    with open('./config/config.json') as json_file:
        config_data = json.load(json_file)
    TG_BOT_API_URL = config_data['TG_BOT_API_URL']
    TG_BOT_TOKEN = config_data['TG_BOT_TOKEN']
    TG_USER_ID = config_data['TG_USER_ID']

    tg_notification_url = f'https://{TG_BOT_API_URL}/bot{TG_BOT_TOKEN}/sendMessage'
    tg_notification_data = {
        'chat_id': TG_USER_ID,
        'text': content,
        'disable_web_page_preview': True
    }
    req = requests.post(tg_notification_url, data=tg_notification_data)

    return req

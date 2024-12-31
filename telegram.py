import os
import requests

from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT = os.getenv('TELEGRAM_BOT')
TELEGRAM_CHAT = os.getenv('TELEGRAM_CHAT')


def send_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage"
    data = {
        'chat_id': TELEGRAM_CHAT,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Уведомление успешно отправлено в Telegram.")
    else:
        print(f"Ошибка при отправке уведомления: {response.status_code}")
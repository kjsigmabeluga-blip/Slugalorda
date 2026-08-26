from flask import Flask, request, abort
import requests
import logging
import threading
import time

app = Flask(__name__)

TOKEN = "8433042361:AAEsweTk9SPc5M2FJd9CNweH9dwv7Sclix0"
SECRET_KEY = "LordSlugaSuperSecretKey123"
MY_IP = "92.101.71.197"

logging.basicConfig(level=logging.INFO)

EXCLUDED_USERS = [
    5268292847,   # Мама
    5318344748,   # Анастасия Игоревна
    1016164154,   # Армася
    1785437636,   # Леся
    -4083558444,  # Большая семья
    -4782064976,  # Мальчики 76
    -5140521238,  # Технология 7 «Б»
    -4581539600,  # Ещё одна группа
]

def is_telegram_ip(ip):
    return ip.startswith('149.154.') or ip.startswith('91.108.')

def self_ping():
    url = "https://slugalorda.onrender.com"
    while True:
        try:
            requests.get(url)
            logging.info("Пинг отправлен")
        except:
            logging.warning("Ошибка пинга")
        time.sleep(30)

threading.Thread(target=self_ping, daemon=True).start()

@app.route('/webhook', methods=['POST'])
def webhook():
    ip = request.remote_addr
    if not is_telegram_ip(ip) and ip != MY_IP:
        logging.warning(f'Доступ запрещён с IP: {ip}')
        abort(403)

    secret = request.headers.get('X-Secret-Key')
    if secret != SECRET_KEY:
        logging.warning(f'Неверный ключ с IP: {ip}')
        abort(403)

    data = request.get_json()
    chat_id = data['message']['chat']['id']
    sender_id = data['message']['from']['id']
    text = data['message'].get('text', '')

    if sender_id in EXCLUDED_USERS:
        logging.info(f'Сообщение от исключённого пользователя {sender_id} — игнорируем')
        return "OK", 200

    if text == '/start':
        active = True
        reply = "✅ Слуга активирован"
    elif text == '/stop':
        active = False
        reply = "⏹️ Слуга отключён"
    elif text == '/status':
        reply = f"✅ Слуга активен: {active}"
    else:
        reply = """эⲧⲟ ⲥⲗⲩⲅⲁ ŁØŘĐŠĦΔĐØŴ Ø₣₣ƗĈƗΔŁ ! Я ⲩⲿⲉ ⳝⲉⲅⲩ ⲕ ⲗⲟⲣⲇⲩ, ⳡⲧⲟⳝы ⲥⲟⲟⳝպυⲧь ⲟ ⲧⲃⲟⲉⲙ ⲃυⳅυⲧⲉ! ⲡⲟⲿⲁⲗⲩύⲥⲧⲁ ⲡⲟⲇⲟⲿⲇυ ⲉⲅⲟ ⲟⲧⲃⲉⲧⲁ!!! ⳝⲗⲁⲅⲟⲇⲁⲣю ⳅⲁ ⲃⲁⲱ ⲃυⳅυⲧ!!"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={'chat_id': chat_id, 'text': reply})
    logging.info(f'Ответ отправлен в чат {chat_id}')
    return "OK", 200

@app.route('/')
def home():
    return "Слуга активен и защищён"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

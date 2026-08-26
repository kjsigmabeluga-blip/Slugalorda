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

def is_telegram_ip(ip):
    return ip.startswith('149.154.') or ip.startswith('91.108.')

# ===== СТУЧАЛКА (каждые 30 секунд) =====
def self_ping():
    url = "https://lord-sluga.onrender.com"  # Замени на свой Render-адрес
    while True:
        try:
            requests.get(url)
            logging.info("Пинг отправлен")
        except:
            logging.warning("Ошибка пинга")
        time.sleep(30)

threading.Thread(target=self_ping, daemon=True).start()

# ===== WEBHOOK =====
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
    text = data['message'].get('text', '')

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

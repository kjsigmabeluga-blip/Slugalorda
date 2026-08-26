from flask import Flask, request, abort
import requests
import logging
import threading
import time

app = Flask(__name__)

TOKEN = "8433042361:AAEsweTk9SPc5M2FJd9CNweH9dwv7Sclix0"
SECRET_KEY = "LordSlugaSuperSecretKey123"

active = True
logging.basicConfig(level=logging.INFO)

EXCLUDED_USERS = [5268292847, 5318344748, 1016164154, 1785437636, -4083558444, -4782064976, -5140521238, -4581539600]

def self_ping():
    url = "https://slugalorda.onrender.com"
    while True:
        try:
            requests.get(url)
        except:
            pass
        time.sleep(30)

threading.Thread(target=self_ping, daemon=True).start()

@app.route('/webhook', methods=['POST'])
def webhook():
    global active

    # Проверка секретного ключа
    secret = request.headers.get('X-Secret-Key')
    if secret != SECRET_KEY:
        abort(403)

    data = request.get_json()
    if 'message' not in data:
        return "OK", 200

    try:
        chat_id = data['message']['chat']['id']
        sender_id = data['message']['from']['id']
        text = data['message'].get('text', '')
    except:
        return "OK", 200

    if sender_id in EXCLUDED_USERS:
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
        reply = "Это слуга LORDSHADOW! Я бегу к лорду, чтобы сообщить о твоём визите! Пожалуйста, подожди!"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={'chat_id': chat_id, 'text': reply})

    return "OK", 200

@app.route('/')
def home():
    return "Слуга активен"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

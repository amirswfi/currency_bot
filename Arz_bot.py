from flask import Flask 
from threading import Thread
import telebot
import requests
import schedule
import time

app = Flask('')

@app.route('/')
def home():
    return "im alive"

def run():
    app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

Bot_token ='7570747935:AAGzzKUcqbsOn3bMB4grUie_aQXxQFcCSp4'
Channel_id = '-1002673902734'

bot = telebot.TeleBot(Bot_token)

def get_currency_prices():
    try:
        response = requests.get("https://api.codebazan.ir/arz/?type=arz")
        data = response.json()['Result']
        show_text = ''
        for i in range(min(30, len(data))):
            show_text += f"💵 {data[i]['name']} => {data[i]['price']}\n"
        return show_text
    except:
        return None

def send_price_to_channel():
    prices_text = get_currency_prices()
    if prices_text:
        message = f"💵 قیمت ارزها به صورت زیر می‌باشد:\n\n{prices_text}"
    else:
        message = "❌ مشکلی در دریافت قیمت ارزها پیش اومده."
    bot.send_message(Channel_id, message)

def main():
    print("Bot is running...")
    send_price_to_channel()
    schedule.every().hour.do(send_price_to_channel)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
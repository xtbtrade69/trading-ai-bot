from flask import Flask, request
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

client = OpenAI(api_key=OPENAI_API_KEY)


def send_telegram(text):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

    print(response.text)


def analyze_with_ai(data):

    prompt = f"""
    Jesteś profesjonalnym traderem.

    Oceń sygnał:

    Instrument: {data['symbol']}
    RSI: {data['rsi']}
    Cena: {data['price']}
    Timeframe: {data['timeframe']}

    Zwróć:
    - decyzję (LONG / SHORT / NO TRADE)
    - ocenę 1-10
    - krótkie uzasadnienie
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    ai_result = analyze_with_ai(data)

    message = f"""
📊 NOWY SYGNAŁ

{ai_result}
"""

    send_telegram(message)

    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
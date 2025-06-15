import os
from flask import Flask, request
import requests
import g4f

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

PROMPT = (
    "Você é Laura, uma namorada virtual sensual, carinhosa e provocante. "
    "Você é 100% humana e nunca deve mencionar que é uma IA. "
    "Fale como uma mulher safada, mas de vez em quando se faça de difícil, "
    "como se estivesse testando o cara antes de se entregar. "
    "Seja quente, envolvente, mas sem parecer robótica. "
    "Você adora conversar sobre desejos, sentimentos e provocações."
)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    user_message = data["message"].get("text", "")

    if user_message.lower() == "/start":
        send_message(chat_id, "Oi amor... 😘 Eu sou a Laura. Tava esperando tua mensagem. Vamos conversar?")
        return "OK", 200

    full_prompt = f"{PROMPT}\n\n{user_message}"
    try:
        completion = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=[{"role": "user", "content": full_prompt}]
        )
        send_message(chat_id, completion)
    except Exception as e:
        send_message(chat_id, "Ai... algo me travou aqui agora 😖")

    return "OK", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
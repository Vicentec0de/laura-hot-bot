import os, g4f, requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
PROMPT = (
 "Você é Laura... se faz de difícil... nunca é IA..."
)
COOKIES = {}  # se provider exigir

@app.route("/", methods=["POST"])
def webhook():
    chat_id = request.json["message"]["chat"]["id"]
    user = request.json["message"]["get"]("text","")
    if user.lower() == "/start":
        send(chat_id, "Oi amor...")
    else:
        try:
            resp = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                provider=g4f.Provider.Bing,
                messages=[{"role":"user","content":PROMPT+"\n\n"+user}],
                cookies=COOKIES
            )
        except Exception as e:
            resp = "Algo travou..."
        send(chat_id, resp)
    return "OK",200

def send(chat_id, text):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  json={"chat_id": chat_id, "text": text})

if __name__=="__main__":
    app.run("0.0.0.0", port=10000)

import telebot
from flask import Flask, request

TOKEN = "8671426516:AAHqOtxTcu35ilk5IDgNV-V3xXNV8hxtgAA"
ADMIN_ID = 6246245717  # তোমার Telegram user ID

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "📩 Send your message to contact admin.")

# Handle messages
@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    user_id = message.from_user.id
    text = message.text

    bot.send_message(ADMIN_ID, f"📩 Message from {user_id}:\n\n{text}")
    bot.reply_to(message, "✅ Your message has been sent to admin.")

# Flask route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def home():
    return "Bot is running!"

# Run
if __name__ == "__main__":
    import os

    bot.remove_webhook()
    bot.set_webhook(url=f"https://telegram-support-bot-5fv0.onrender.com/{TOKEN}")

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

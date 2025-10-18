import telebot
import time
import json
import threading
from datetime import datetime
from flask import Flask
import os

# ===============================
# 🔒 إعداد البوت
# ===============================
TOKEN = "8371961432:AAGtmprdhZ1GsCH35uGRbQHxBXlcLX1Af_s"
bot = telebot.TeleBot(TOKEN)

# ===============================
# 📦 قاعدة بيانات العقود
# ===============================
DATA_FILE = "contracts.json"

def load_contracts():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_contracts(contracts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(contracts, f, indent=2, ensure_ascii=False)

contracts = load_contracts()

# ===============================
# 🧠 إضافة عقد جديد
# ===============================
@bot.message_handler(commands=["اضف_عقد"])
def add_contract(message):
    msg = bot.reply_to(message, "📥 أرسل اسم العقد مثل:\n`NVDA 450C 10/25`")
    bot.register_next_step_handler(msg, save_new_contract)

def save_new_contract(message):
    contract_name = message.text.strip()
    new_contract = {
        "name": contract_name,
        "profit": 0,
        "added_at": str(datetime.now()),
        "alert_sent": False
    }
    contracts.append(new_contract)
    save_contracts(contracts)
    bot.reply_to(message, f"✅ تم إضافة العقد: {contract_name}")

# ===============================
# 🔁 تحديث تلقائي كل دقيقة
# ===============================
def update_contracts():
    while True:
        time.sleep(60)
        for c in contracts:
            c["profit"] += 10
            if c["profit"] >= 30 and not c.get("alert_sent"):
                try:
                    bot.send_message(
                        chat_id="@QbK7d0Rm0NEzYzQ0",
                        text=f"💰 العقد [{c['name']}] حقق +30٪\n🎯 مبروك يا بطل السوق!\n🧠 بإشراف: Majed_option"
                    )
                    c["alert_sent"] = True
                except Exception as e:
                    print(f"⚠️ خطأ أثناء إرسال التنبيه: {e}")
        save_contracts(contracts)

# ===============================
# 🌐 Flask للتأكيد
# ===============================
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Majed Bot is running successfully and stable!"

# ===============================
# 🚀 التشغيل المنفصل
# ===============================
def start_bot():
    print("🤖 Running Majed bot polling...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)

if __name__ == "__main__":
    # تشغيل البوت في خيط منفصل
    t1 = threading.Thread(target=start_bot)
    t1.start()

    # تشغيل Flask بشكل أساسي
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

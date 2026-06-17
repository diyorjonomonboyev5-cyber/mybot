from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

BOT_TOKEN = "8610613439:AAGaNi2DM65tOeoJoATiMXImsORBXbQNXgE"
API_KEY = "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"

def chat_ai(text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Sen faqat o‘zbek tilida javob berasan."},
            {"role": "user", "content": text}
        ]
    }

    r = requests.post(url, headers=headers, json=data)
    return r.json()["choices"][0]["message"]["content"]

def image_ai(prompt):
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "1024x1024"
    }

    r = requests.post(url, headers=headers, json=data)
    return r.json()["data"][0]["url"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom 🤖 Men AI botman!\n💬 yoz → javob beraman\n🖼 /img → rasm chizaman")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text.startswith("/img"):
        prompt = text.replace("/img", "").strip()
        url = image_ai(prompt)
        await update.message.reply_photo(photo=url)
    else:
        answer = chat_ai(text)
        await update.message.reply_text(answer)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()

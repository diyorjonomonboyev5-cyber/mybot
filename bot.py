import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

BOT_TOKEN = os.getenv("8610613439:AAGaNi2DM65tOeoJoATiMXImsORBXbQNXgE")
OPENAI_API_KEY = os.getenv("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")

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ishlayapti!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    res = client.responses.create(
        model="gpt-4.1-mini",
        input=update.message.text
    )
    await update.message.reply_text(res.output_text)

async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)

    if not prompt:
        await update.message.reply_text("Misol: /img cyberpunk city")
        return

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    await update.message.reply_photo(photo=result.data[0].url)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("img", img))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()

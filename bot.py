
import os
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from config import TOKEN, ADMIN_ID
from modules.downloader import download_video

DB_FILE = "database.json"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    with open(DB_FILE) as f:
        db = json.load(f)

    if user not in db["users"]:
        db["users"].append(user)
        with open(DB_FILE,"w") as f:
            json.dump(db,f)

    keyboard = [
        [InlineKeyboardButton("📥 تحميل فيديو", callback_data="video")],
        [InlineKeyboardButton("🎵 تحميل صوت", callback_data="mp3")],
        [InlineKeyboardButton("📚 ستوري انستغرام", callback_data="story")]
    ]

    await update.message.reply_text(
        "اهلا بك في بوت تحميل السوشال ميديا\nارسل رابط الفيديو للتحميل.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    msg = await update.message.reply_text("⏳ جاري التحميل...")

    try:
        file = download_video(url)
        await update.message.reply_video(video=open(file,"rb"))
        os.remove(file)
        await msg.delete()

    except Exception as e:
        await update.message.reply_text("❌ فشل تحميل الفيديو")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    with open(DB_FILE) as f:
        db = json.load(f)

    await update.message.reply_text(f"عدد المستخدمين: {len(db['users'])}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("Bot Running...")

app.run_polling()

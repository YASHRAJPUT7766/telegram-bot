import telebot
import yt_dlp
import os

# यहाँ अपना Telegram Bot Token डालें
BOT_TOKEN = "7764415796:AAEndEYGBZS5UJZUWY19nwBxgdT4c5G_15M"

# Telegram Bot इनिशियलाइज़ करें
bot = telebot.TeleBot(BOT_TOKEN)

 
# ✅ जिस चैनल को जॉइन कराना है उसका username  
CHANNEL_USERNAME = "@theREALP4x" 

# ✅ Function to check if user is a member of the channel
def is_user_subscribed(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False
    except:
        return False

# ✅ Handle /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id

    if is_user_subscribed(user_id):
        bot.reply_to(message, "✅ Welcome! You have successfully joined the channel. Now send me a YouTube link.")
    else:
        bot.reply_to(
            message,
            f"⚠️ You must join our channel first to use this bot!\n\n👉 [Join Now](https://t.me/{CHANNEL_USERNAME[1:]})\n\nThen click /start again.",
            parse_mode="Markdown"
        )
        return  # Stop execution if user is not subscribed

# ✅ Handle YouTube video download requests
@bot.message_handler(func=lambda message: True)
def download_video(message):
    user_id = message.from_user.id

    # ✅ सबसे पहले यूजर को चेक करें कि उसने चैनल जॉइन किया है या नहीं
    if not is_user_subscribed(user_id):
        bot.reply_to(
            message,
            f"⚠️ You must join our channel first to use this bot!\n\n👉 [Join Now](https://t.me/{CHANNEL_USERNAME[1:]})\n\nThen click /start again.",
            parse_mode="Markdown"
        )
        return  # Stop execution if user is not subscribed

    url = message.text

    # ✅ yt-dlp सेटिंग्स
    ydl_opts = {
        'format': 'best[filesize<50M]',  # 50MB से छोटे वीडियो डाउनलोड होंगे
        'outtmpl': 'downloaded_video.%(ext)s',
    }

    try:
        # ✅ वीडियो डाउनलोड करें
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # ✅ डाउनलोड की गई फाइल को भेजें
        for file in os.listdir():
            if file.startswith("downloaded_video"):
                with open(file, "rb") as video:
                    bot.send_video(message.chat.id, video)

                # ✅ वीडियो भेजने के बाद फाइल डिलीट करें
                os.remove(file)
                break

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# ✅ बॉट को रन करें
print("Bot is running...")
bot.polling()
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! Send me a YouTube link to download the video.")
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext
import yt_dlp

# लॉगिंग सेटअप
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# यूट्यूब वीडियो डाउनलोड करने का फंक्शन
def get_video_formats(url):
    ydl_opts = {"quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = []
        for f in info["formats"]:
            if f.get("format_note") and f.get("url"):
                formats.append((f["format_note"], f["url"]))  # (क्वालिटी, डाउनलोड URL)
        return formats

# स्टार्ट कमांड
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("YouTube वीडियो डाउनलोड करने के लिए लिंक भेजें।")

# जब यूजर यूट्यूब लिंक भेजे
async def receive_link(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        formats = get_video_formats(url)
        if not formats:
            await update.message.reply_text("कोई डाउनलोड करने योग्य फॉर्मेट नहीं मिला।")
            return
        
        # क्वालिटी ऑप्शन्स के लिए बटन बनाना
        keyboard = [
            [InlineKeyboardButton(f"{q}p", callback_data=url + "|" + u)] for q, u in formats if q.isdigit()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("कृपया डाउनलोड करने की क्वालिटी चुनें:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("कृपया एक मान्य YouTube वीडियो लिंक भेजें।")

# जब यूजर क्वालिटी चुने
async def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    url, download_url = query.data.split("|")

    # यूजर को डाउनलोड लिंक भेजना
    await query.message.reply_text(f"आपका वीडियो तैयार है:\n[डाउनलोड करें]({download_url})", parse_mode="Markdown")

# मेन फंक्शन (बॉट स्टार्ट करने के लिए)
def main():
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # यहाँ अपना टेलीग्राम बॉट का टोकन डालें
    app = Application.builder().token(TOKEN).build()

    # हैंडलर्स जोड़ें
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_link))
    app.add_handler(CallbackQueryHandler(button_callback))

    # बॉट को चलाएँ
    app.run_polling()

if __name__ == "__main__":
    main()
def download_video(message):
    url = message.text

    # yt-dlp सेटिंग्स
    ydl_opts = {
        'format': 'best[filesize<50M]',  # 50MB से छोटे वीडियो डाउनलोड होंगे
        'outtmpl': 'downloaded_video.%(ext)s',
    }

    try:
        # वीडियो डाउनलोड करें
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # डाउनलोड की गई फाइल को भेजें
        for file in os.listdir():
            if file.startswith("downloaded_video"):
                with open(file, "rb") as video:
                    bot.send_video(message.chat.id, video)

                # वीडियो भेजने के बाद फाइल डिलीट करें
                os.remove(file)
                break

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# बॉट को रन करें
print("Bot is running...")
bot.polling()
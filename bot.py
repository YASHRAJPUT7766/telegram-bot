import telebot
import yt_dlp
import os

# यहाँ अपना Telegram Bot Token डालें
BOT_TOKEN = "7764415796:AAEwjQT5GbRs-WxczGVZn8DOvGc3ha8W8Jo"

bot = telebot.TeleBot(BOT_TOKEN)  # यह लाइन वापस जोड़ें

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! Send me a YouTube link to download the video.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text

    # yt-dlp settings
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Send video to user
        with open("downloaded_video.mp4", "rb") as video:
            bot.send_video(message.chat.id, video)

        # Delete video after sending
        os.remove("downloaded_video.mp4")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")

# Start bot
bot.infinity_polling()
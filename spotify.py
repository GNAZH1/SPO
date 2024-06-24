from almgroad import Spotify_Download
import telebot, os, requests, re
from telebot import types
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


bot = telebot.TeleBot("7218709784:AAEUPP94r4WKTNZwbN1IzJzVZ5eXe8mvQ9s")

# @GNA_I
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def save_photo(url):
    bb = session.get(url).content
    with open("photo.jpg", "wb") as d:
        d.write(bb)

def save_mp3(url):
    bb = session.get(url).content
    with open("audio.mp3", "wb") as d:
        d.write(bb)

def is_spotify_url(url):
    spotify_pattern = re.compile(r'https?://open\.spotify\.com/track/[a-zA-Z0-9]+')
    return bool(spotify_pattern.match(url))

@bot.message_handler(commands=["start"])
def first(message):
    markup = types.InlineKeyboardMarkup()
    btn_contact = types.InlineKeyboardButton(text="📞 المطور", url=f"https://t.me/GNA_I")
    markup.add(btn_contact)
    bot.reply_to(message, "👋 أهلًا وسهلًا بك في بوت تحميل الموسيقى من سبوتيفاي! 🎵\nأرسل رابط الأغنية من Spotify وانتظر قليلًا لتحميلها.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def two(message):
    if is_spotify_url(message.text):
        down = Spotify_Download(message.text)
        save_photo(down["photo"])

        #@GNA_I
        markup = types.InlineKeyboardMarkup()
        btn_download = types.InlineKeyboardButton(text="📥 تنزيل", callback_data="download")
        btn_cancel = types.InlineKeyboardButton(text="❌ إلغاء", callback_data="cancel")
        markup.add(btn_download, btn_cancel)

        
        bot.send_photo(message.chat.id, open("photo.jpg", "rb"), caption="🎵 تم العثور على الأغنية. اختر إجراء:", reply_markup=markup)

     #@GNA_I
        bot.user_data[message.chat.id] = down
    else:
        bot.reply_to(message, "❌ هذا ليس رابط سبوتيفاي. يرجى إرسال رابط أغنية من Spotify.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "download":
        down = bot.user_data.pop(call.message.chat.id, None)
        if down:
            a = bot.send_message(call.message.chat.id, "⏳ انتظر قليلًا ...")
            save_mp3(down["url"])
            bot.send_audio(call.message.chat.id, open("audio.mp3", "rb"), title=down["title"], performer=down["artist"], thumb=open("photo.jpg", "rb"))
            bot.delete_message(call.message.chat.id, a.message_id)
            os.remove("audio.mp3")
            os.remove("photo.jpg")
    elif call.data == "cancel":
        bot.send_message(call.message.chat.id, "🚫 تم إلغاء العملية.")

print("Running...")
bot.user_data = {}  #@GNA_I
bot.infinity_polling(timeout=60, long_polling_timeout=60)

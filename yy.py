import os
import json
import time
import telebot
import asyncio
import requests
from telethon import TelegramClient, functions, types, errors
from datetime import datetime
import json
import random
from telethon import TelegramClient, errors, functions, types
from telethon.sessions import StringSession
import aiohttp
import string
import telebot
from telebot import types
from user_agent import generate_user_agent

API_ID = 26957529
API_HASH = 'ffe7d862b0a31893682a62bbc0654ced'
BOT_TOKEN = '6383532072:AAGkOq2B-0gcVwwv8OI6l_N2v13SsaxqqD0' #توكنك
ADMIN_CHAT_ID = 5089141183
SESSIONS_DIR = './sessions'

bot = telebot.TeleBot(BOT_TOKEN)

VIP_USERS_FILE = 'vip_users.txt'
BANNED_USERS_FILE = 'banned_users.txt'
ADMINS_FILE = 'admins.txt'
SESSIONS_FILE = './sessions'

if not os.path.exists('sessions'):
    os.makedirs('sessions')

USERNAMES_DIRECTORY = 'usernames'
if not os.path.exists(USERNAMES_DIRECTORY):
    os.makedirs(USERNAMES_DIRECTORY)

if not os.path.exists('users'):
    with open('users', 'w') as f:
        f.write('')
        
if not os.path.exists(VIP_USERS_FILE):
    with open(VIP_USERS_FILE, 'w') as f:
        f.write('')

if not os.path.exists(BANNED_USERS_FILE):
    with open(BANNED_USERS_FILE, 'w') as f:
        f.write('')

if not os.path.exists(ADMINS_FILE):
    with open(ADMINS_FILE, 'w') as f:
        f.write('')

def is_admin(user_id):
    admins = []
    with open(ADMINS_FILE, 'r') as f:
        f = f.read().split()
        admins.append(f)
    if user_id in admins[0] :
        return str(user_id) in admins

def add_admin(user_id):
    with open(ADMINS_FILE, 'a') as f:
        f.write(str(user_id) + '\n')

def remove_admin(user_id):
    with open(ADMINS_FILE, 'r') as f:
        admins = f.read().splitlines()
    with open(ADMINS_FILE, 'w') as f:
        for admin in admins:
            if admin != str(user_id):
                f.write(admin + '\n')
                
def is_vip(user_id):
    with open(VIP_USERS_FILE, 'r') as f:
        vip_users = f.read().splitlines()
    return str(user_id) in vip_users

def is_banned(user_id):
    with open(BANNED_USERS_FILE, 'r') as f:
        banned_users = f.read().splitlines()
    return str(user_id) in banned_users

def add_vip(user_id):
    with open(VIP_USERS_FILE, 'a') as f:
        f.write(str(user_id) + '\n')

def remove_vip(user_id):
    with open(VIP_USERS_FILE, 'r') as f:
        vip_users = f.read().splitlines()
    with open(VIP_USERS_FILE, 'w') as f:
        for user in vip_users:
            if user != str(user_id):
                f.write(user + '\n')

def add_banned(user_id):
    with open(BANNED_USERS_FILE, 'a') as f:
        f.write(str(user_id) + '\n')

def remove_banned(user_id):
    with open(BANNED_USERS_FILE, 'r') as f:
        banned_users = f.read().splitlines()
    with open(BANNED_USERS_FILE, 'w') as f:
        for user in banned_users:
            if user != str(user_id):
                f.write(user + '\n')
                
if os.path.exists('data.json'):
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
else:
    data = {"usernames": [], "files": []}

def save_data():
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

main_loop = asyncio.get_event_loop()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_banned(message.chat.id):
        bot.send_message(message.chat.id, "أنت محظور من استخدام هذا البوت 🚫")
        return

    if not is_vip(message.chat.id):
        markup = telebot.types.InlineKeyboardMarkup()
        subscribe_vip = telebot.types.InlineKeyboardButton(text="تقديم طلب", callback_data="subscribe_vip")
        markup.add(subscribe_vip)
        bot.send_message(message.chat.id, "عذرا قدم طلب للحصول على صلاحية استخدام الروبوت عن طريق الزر الموجود بالاسفل.", reply_markup=markup)
        return

    markup = telebot.types.InlineKeyboardMarkup()
    login = telebot.types.InlineKeyboardButton(text="- اضف حساب", callback_data="login")
    GETT = telebot.types.InlineKeyboardButton(text="- قسم الجلسات", callback_data="show_menu")
    accounts = telebot.types.InlineKeyboardButton(text="- حساباتك", callback_data="session_files")
    add_user = telebot.types.InlineKeyboardButton(text="- قسم الخاصيه", callback_data="fahs")
    tys_rand = telebot.types.InlineKeyboardButton(text="- الصيد العشوائي", callback_data="random_capture")
    add_file = telebot.types.InlineKeyboardButton(text="- اضف ملف", callback_data="add_files")
    files = telebot.types.InlineKeyboardButton(text="- ملفاتي", callback_data="files")
    check_file = telebot.types.InlineKeyboardButton(text="- فحص ملف", callback_data="check_file")
    dev = telebot.types.InlineKeyboardButton(text="- DEV", url="t.me/GNA_I")
    channel = telebot.types.InlineKeyboardButton(text="- SOURCE", url="t.me/SOURCE_GNAZH")

    markup.add(login, accounts)
    markup.add(GETT)
    markup.add(add_file)
    markup.add(check_file, files)
    markup.add(add_user, tys_rand)
    markup.add(dev, channel)

    bot.send_message(message.chat.id, "مرحبا بك في سورس جنازه لفحص وصيد اليوزرات 🌊\n\n① بوت فحص وصيد يوزرات 👨‍🔧\n② صيد يوزرات خاصيه 🕵️‍♂️\n③ صيد يوزرات حذف 🗑\n④ صيد عشوائي مفحوص ✅ \n\n⑤ يتم حجز اليوزر المتاح في قناة 🚀", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "subscribe_vip")
def subscribe_vip(call):
    msg = bot.send_message(call.message.chat.id, "- يرجى تفعيل البوت من المطور ❲ @GNA_I ❳\n\n- او ارسل /nedbot")
    bot.register_next_step_handler(msg, process_vip_subscription)

def process_vip_subscription(message):
    user_id = message.chat.id
    sent_number = message.text
    markup = telebot.types.InlineKeyboardMarkup()
    approve_vip = telebot.types.InlineKeyboardButton(text="- تفعيل", callback_data=f"approve_vip_{user_id}")
    reject_vip = telebot.types.InlineKeyboardButton(text="- رفض", callback_data=f"reject_vip_{user_id}")
    markup.add(approve_vip, reject_vip)
    bot.send_message(ADMIN_CHAT_ID, f"طلب جديد لتفعيل البوت:\n\nايدي المستخدم : {user_id}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_vip_"))
def approve_vip(call):
    user_id = call.data.split("_")[2]
    add_vip(user_id)
    bot.send_message(user_id, "تمت الموافقة على طلب تفعيلك. يمكنك الآن استخدام البوت.")
    bot.send_message(call.message.chat.id, f"تم السماح للمستخدم {user_id}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("reject_vip_"))
def reject_vip(call):
    user_id = call.data.split("_")[2]
    bot.send_message(user_id, "تم رفض طلب تفعيل البوت الخاص بك.")
    bot.send_message(call.message.chat.id, f"تم رفض التفعيل للمستخدم {user_id}")

@bot.callback_query_handler(func=lambda call: call.data == "fahs")
def fahs(call):
    markup = telebot.types.InlineKeyboardMarkup()
    add_user_button = telebot.types.InlineKeyboardButton(text="- اضف يوزر", callback_data="add_user")
    saved_users_button = telebot.types.InlineKeyboardButton(text="- يوزراتك", callback_data="show_users")
    check_users_button = telebot.types.InlineKeyboardButton(text="- بدأ الفحص", callback_data="check_users")
    back = telebot.types.InlineKeyboardButton(text="رجـــوع 🔙", callback_data="back")
    markup.add(add_user_button, check_users_button)
    markup.add(saved_users_button)
    markup.add(back)
    bot.edit_message_text("مرحبا بك! في قسم الخاصيه 🌊👨‍🔧\n\n• عندما يصبح يوزر متاح يرسل البوت لك رسالة بوقت اليوزر وعند انتهاء مدة التعليق يحجزه في قناة فوراً 🚀", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

user_session_folder = 'sessions'

@bot.callback_query_handler(func=lambda call: call.data == "login")
def login(call):
    user_id = call.from_user.id
    
    if not os.path.exists(user_session_folder):
        os.makedirs(user_session_folder)

    bot.send_message(call.message.chat.id, "أرسل رقم الحساب الذي تريد اضافته مع رمز الدولة 📞\n\n مثال : +2012110000000")
    bot.register_next_step_handler(call.message, process_phone_number, user_id)

def process_phone_number(message, user_id):
    phone = message.text.replace(" ", "")
    bot.send_message(message.chat.id, "⏳")
    main_loop.run_until_complete(handle_phone_number(message, phone, user_id))

async def handle_phone_number(message, phone, user_id):
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            bot.send_message(message.chat.id, "تم ارسال كود تحقق الى الحساب .. ارسله لي 💬")
            bot.register_next_step_handler(message, lambda m: main_loop.run_until_complete(handle_code(m, client, user_id, phone)))
        except Exception as e:
            bot.send_message(message.chat.id, f"An error occurred: {str(e)}")
    else:
        bot.send_message(message.chat.id, "هذا الرقم مسجل بالفعل ⚠️")
    await client.disconnect()

async def handle_code(message, client, user_id, phone):
    code = message.text.replace(" ", "")
    try:
        await client.connect()
        await client.sign_in(phone=phone, code=code)
        if await client.is_user_authorized():
            string_session = client.session.save()
            save_session(user_id, phone, string_session)
            bot.send_message(message.chat.id, "تم تسجيل الحساب بنجاح ✅")
        else:
            bot.send_message(message.chat.id, "الحساب محمي بالتحقق بخطوتين .. أرسل كلمة المرور لاستكمال عملية تسجيل الدخول 🔐")
            bot.register_next_step_handler(message, lambda m: main_loop.run_until_complete(handle_password(m, client, user_id, phone)))
    except errors.SessionPasswordNeededError:
        bot.send_message(message.chat.id, "الحساب محمي بالتحقق بخطوتين .. ارسل كلمة السر 🔐")
        bot.register_next_step_handler(message, lambda m: main_loop.run_until_complete(handle_password(m, client, user_id, phone)))
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")
    finally:
        await client.disconnect()

async def handle_password(message, client, user_id, phone):
    password = message.text
    try:
        await client.connect()
        await client.sign_in(password=password)
        if await client.is_user_authorized():
            string_session = client.session.save()
            save_session(user_id, phone, string_session, password)
            bot.send_message(message.chat.id, "تم اضافة الحساب بنجاح ✅")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")
    finally:
        await client.disconnect()

def save_session(user_id, phone, session, password=None):
    file_path = f'{user_session_folder}/{user_id}.json'
    data = {"phone_number": phone, "two-step": password if password else "لا يوجد", "session": session}
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            existing_data.append(data)
    else:
        existing_data = [data]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

USERS_DIRECTORY = 'user_data'


@bot.callback_query_handler(func=lambda call: call.data == "show_menu")
def show_menu(call):
    markup = types.InlineKeyboardMarkup()
    get_session_button = types.InlineKeyboardButton(text="جلب جلسة برقم الهاتف", callback_data="get_session")
    get_all_sessions_button = types.InlineKeyboardButton(text="جلب جميع الجلسات", callback_data="get_all_sessions")
    back = telebot.types.InlineKeyboardButton(text="رجـــوع 🔙", callback_data="back")
    markup.add(get_session_button, get_all_sessions_button)
    markup.add(back)
    bot.edit_message_text("اختر العملية التي تريد تنفيذها:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda event: event.data == "get_session")
def get_session(event):
    start_time = time.time()
    bot.send_message(event.message.chat.id, "- ارسل الان رقم الهاتف الذي قمت بتسجيله للبوت لجلب الجلسة منه")
    
    bot.register_next_step_handler(event.message, process_phone_session, start_time)

def process_phone_session(message, start_time):
    phone_number = message.text.replace("+", "").replace(" ", "")
    user_id = message.from_user.id
    file_path = f'sessions/{user_id}.json'
    
    if not os.path.exists(file_path):
        bot.send_message(message.chat.id, "- لم يتم العثور على هذا الرقم ضمن قائمة الحسابات")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        accounts = json.load(f)
    
    for account in accounts:
        stored_phone_number = account['phone_number'].replace("+", "").replace(" ", "")
        if phone_number == stored_phone_number:
            text = f'''• رقم الهاتف : {account['phone_number']}\n\n- التحقق بخطوتين : {account['two-step']}\n\n- الجلسة : `{account['session']}`'''
            stop_time = time.time() - start_time
            text += f"\n**- الوقـت المستغـرق 📟 :** {stop_time:.02f} **ثـانيـه**"
            bot.send_message(message.chat.id, text)
            return
    
    bot.send_message(message.chat.id, "- لم يتم العثور على هذا الرقم ضمن قائمة الحسابات")

@bot.callback_query_handler(func=lambda event: event.data == "get_all_sessions")
def get_all_sessions(event):
    start_time = time.time()
    user_id = event.from_user.id
    file_path = f'sessions/{user_id}.json'
    
    if not os.path.exists(file_path):
        bot.send_message(event.message.chat.id, "- لم يتم العثور على أي جلسات ضمن قائمة الحسابات")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        accounts = json.load(f)
    
    text = "قائمة الجلسات المخزنة:\n\n"
    for account in accounts:
        text += f'''• رقم الهاتف : {account['phone_number']}\n- تحقق بخطوتين : {account['two-step']}\n- الجلسة : `{account['session']}`\n\n'''
    
    stop_time = time.time() - start_time
    text += f"\n**- الوقت المستغرق :** {stop_time:.02f} **ثانيه**"

    if len(text) > 4096:
        file_name = f'sessions_{user_id}.txt'
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(text)
        
        with open(file_name, 'rb') as file:
            bot.send_document(event.message.chat.id, file)
        
        os.remove(file_name)
    else:
        bot.send_message(event.message.chat.id, text)



@bot.callback_query_handler(func=lambda call: call.data == "show_users")
def show_users(call):
    user_id = call.from_user.id
    file_path = os.path.join(USERNAMES_DIRECTORY, f'{user_id}.json')

    markup = telebot.types.InlineKeyboardMarkup()
    
    delete_all_button = telebot.types.InlineKeyboardButton(text="- حذف الكل", callback_data="delete_all_users")
    markup.add(delete_all_button)
    
    delete_user_button = telebot.types.InlineKeyboardButton(text="- حذف يوزر", callback_data="delete_user")
    markup.add(delete_user_button)
    
    back_button = telebot.types.InlineKeyboardButton(text="رجـــوع 🔙", callback_data="private_section")
    markup.add(back_button)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            users = json.load(f)
        
        if users:
            users_list = "• @" + "\n• @".join(users)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"يوزراتك المضافة للفحص 📜\n\n@{users_list}", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, "لم يتم إضافة أي يوزرات بعد ❌")
    
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "لم يتم إضافة أي يوزرات بعد ❌")

@bot.callback_query_handler(func=lambda call: call.data == "private_section")
def private_section(call):
    fahs(call)

@bot.callback_query_handler(func=lambda call: call.data == "add_user")
def add_user(call):
    bot.send_message(call.message.chat.id, "أرسل اليوزر بدون @ لإضافته إلى قائمة الفحص 🔬")
    bot.register_next_step_handler(call.message, save_user)

def save_user(message):
    user_id = message.from_user.id
    username = message.text.replace("@", "")
    file_path = os.path.join(USERNAMES_DIRECTORY, f'{user_id}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            users = json.load(f)
    else:
        users = []

    users.append(username)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

    bot.send_message(message.chat.id, f"تم إضافة اليوزر إلى قائمة الفحص ✅\n\n• اليوزر : @{username}\n\nعندما يتوفر سأحجزه في القناة 🐊")

@bot.callback_query_handler(func=lambda call: call.data == "delete_user")
def delete_user_prompt(call):
    bot.send_message(call.message.chat.id, "أرسل اليوزر الذي تريد حذفه من القائمة")
    bot.register_next_step_handler(call.message, delete_user)

def delete_user(message):
    user_id = message.from_user.id
    username = message.text.replace("@", "")
    file_path = os.path.join(USERNAMES_DIRECTORY, f'{user_id}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            users = json.load(f)
        
        if username in users:
            users.remove(username)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=4)
            bot.send_message(message.chat.id, f"تم حذف اليوزر @{username} من القائمة ✅")
        else:
            bot.send_message(message.chat.id, f"اليوزر @{username} غير موجود في القائمة ❌")
    else:
        bot.send_message(message.chat.id, "لم يتم العثور على أي يوزرات لحذفها ❌")

@bot.callback_query_handler(func=lambda call: call.data == "delete_all_users")
def delete_all_users(call):
    user_id = call.from_user.id
    file_path = os.path.join(USERNAMES_DIRECTORY, f'{user_id}.json')

    if os.path.exists(file_path):
        os.remove(file_path)
        bot.send_message(call.message.chat.id, "تم حذف جميع اليوزرات 🗑️")
    else:
        bot.send_message(call.message.chat.id, "لم يتم العثور على أي يوزرات لحذفها ❌")


@bot.callback_query_handler(func=lambda call: call.data == "check_users")
def check_users(call):
    bot.send_message(call.message.chat.id, "تم بدأ فحص الخاصية 🐊")

    user_id = call.from_user.id
    file_path = os.path.join(USERNAMES_DIRECTORY, f'{user_id}.json')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            users = json.load(f)
        
        sessions = get_session_files(user_id)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = []
        
        for session in sessions:
            task = asyncio.ensure_future(check_usernames(users, session, call.message.chat.id, None))
            tasks.append(task)
        
        loop.run_until_complete(asyncio.gather(*tasks))
        
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "لم يتم إضافة أي يوزرات بعد ❌")

@bot.callback_query_handler(func=lambda call: call.data == "add_files")
def add_files(call):
    bot.send_message(call.message.chat.id, "أرسل الملف لإضافته إلى قائمتك الخاصة 🐊")
    bot.register_next_step_handler(call.message, save_user_file)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    save_user_file(message)

def save_user_file(message):
    user_id = message.from_user.id
    
    if message.document:
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            user_file_path = os.path.join(USERS_DIRECTORY, f'{user_id}_file_{message.document.file_name}')
            
            if not os.path.exists(USERS_DIRECTORY):
                os.makedirs(USERS_DIRECTORY)
            
            with open(user_file_path, 'wb') as f:
                f.write(downloaded_file)
                
            # قراءة المحتوى وتحديث البيانات
            with open(user_file_path, 'r', encoding='utf-8') as f:
                usernames = f.read().strip().split('\n')
                
            
            data["files"].append({
                "user_id": user_id,
                "filename": message.document.file_name,
                "checking": False,
                "usernames": usernames
            })
            save_data()
            
            bot.send_message(message.chat.id, f"تم إضافة الملف إلى قائمتك الخاصة ✅\n\n• اسم الملف : {message.document.file_name}")
        
        except Exception as e:
            bot.send_message(message.chat.id, f"حدث خطأ أثناء تحميل الملف ❌\n\n• الخطأ: {str(e)}")
    else:
        bot.send_message(message.chat.id, "لم يتم استلام أي ملف. حاول مرة أخرى ⚠️")


def check_user(username):
    url = "https://t.me/"+str(username)
    headers = {
        "User-Agent": generate_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7"}

    response = requests.get(url, headers=headers)
    if response.text.find('If you have <strong>Telegram</strong>, you can contact <a class="tgme_username_link"') >= 0:
        return "Available"
    else:
        return "Unavailable"

@bot.callback_query_handler(func=lambda call: call.data == "check_file")
def check_file(call):
    bot.send_message(call.message.chat.id, "ارسل الملف الذي تريد فحص اليوزرات الموجودة بداخله 📂")
    bot.register_next_step_handler(call.message, lambda message: process_file(message, None))

async def create_channel(client):
    channel_title = "SouRce WeVy 🌊"
    try:
        ch = await client(functions.channels.CreateChannelRequest(
            title=channel_title,
            about='تم حجز هذه القناة بواسطة سورس جنازه لصيد الخاصيه والفحص لشراء او الاشتراك في السورس ~» @GNA_I',
            megagroup=False
        ))
        return ch.chats[0].id
    except Exception as e:
        print(f"Error creating channel: {e}")
        return None

@bot.callback_query_handler(func=lambda call: call.data == "random_capture")
def random_capture(call):
    bot.send_message(call.message.chat.id, "- تم بدأ الصيد العشوائي بنجاح 🐊")
    asyncio.run(process_random_capture(call))

async def process_random_capture(call):
    user_id = call.from_user.id
    sessions = get_session_files(user_id)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []

    for session in sessions:
        
        task = asyncio.ensure_future(random_capture_with_session(session, call.message.chat.id))
        tasks.append(task)

    await asyncio.gather(*tasks)

async def random_capture_with_session(session, chat_id):
    async with TelegramClient(StringSession(session['session']), API_ID, API_HASH) as client:
        channel_id = None
        while True:
            random_pattern = random.randint(1, 17)
            random_username = generate_random_username(random_pattern)
            
            isav = check_user(random_username)
            if "Available" in isav:
                if channel_id is None:
                    channel_id = await create_channel(client)
                    if channel_id is None:
                        bot.send_message(chat_id, "Failed to create channel.")
                        return
                    
                try:
                    await client(functions.channels.UpdateUsernameRequest(
                        channel=channel_id,
                        username=random_username
                    ))
                    now = datetime.now()
                    current_time = now.strftime("%H:%M")
                    bot.send_message(ADMIN_CHAT_ID, f"- قام مشترك بصيد يوزر عشوائي .\n\n• اليوزر : @{random_username} \n• الوقت : {current_time}\n\n- وتم حجزه في قناة بنجاح ")
                    bot.send_message(chat_id, f"تم صيد يوزر عشوائي ✅\n\n• اليوزر : @{random_username} \n• الوقت : {current_time}\n\n- وتم حجزه في قناة بنجاح ")
                    channel_id = None
                    break
                except errors.ChannelsAdminPublicTooMuchError:
                    bot.send_message(chat_id, f"خطأ بصيد اليوزر @{random_username} \n\n السبب : \n أنت مسؤول في عدد كبير جدًا من القنوات العامة. يرجى جعل بعض القنوات خاصة لتغيير اسم المستخدم لهذه القناة.")
                    break
                except errors.FloodWaitError as e:
                    bot.send_message(chat_id, f"حساب الفحص مبند لمدة {e.seconds} ثانية.")
                    await asyncio.sleep(e.seconds)
                except errors.rpcerrorlist.UsernameInvalidError:
                    pass
                except Exception as e:
                    pass

a = 'qwertyuiopasdfghjklzxcvbnm'
b = '1234567890'
e = 'qwertyuiopasdfghjklzxcvbnm1234567890'
def generate_random_username(choice):
    while True:
        if choice == 1: # or choice == "ثلاثي_مختلط":
            c = random.choices(a)
            d = random.choices(b)
            s = random.choices(e)
            f = [c[0], "_", d[0], "_", s[0]]
            username = ''.join(f)
        elif choice == 2: # or choice == "ثلاثي":
            c = random.choices(a)
            d = random.choices(a)
            s = random.choices(e)
            f = [c[0], "_", d[0], "_", s[0]]
            username = ''.join(f)
        elif choice == 3: # or choice == "vip_رقمين":
            c = random.choices(b)
            d = random.choices(b)
            f = [c[0], d[0]]
            random.shuffle(f)
            username = 'vip' + ''.join(f)
        elif choice == 4: # or choice == "vip_ثلاث_ارقام":
            c = random.choices(b)
            d = random.choices(b)
            s = random.choices(b)
            f = [c[0], d[0], s[0]]
            random.shuffle(f)
            username = 'vip' + ''.join(f)
        elif choice == 5: # or choice == "خماسي_حرف":
            c = d = random.choices(a)
            d = random.choices(b)
            f = [c[0], d[0], c[0], c[0], c[0]]
            random.shuffle(f)
            username = ''.join(f)
        elif choice == 6: # or choice == "خماسي_حرفين":
            c = d = random.choices(a)
            d = random.choices(b)
            f = [c[0], d[0], c[0], c[0], d[0]]
            random.shuffle(f)
            username = ''.join(f)
        elif choice == 7: # or choice == "سداسي_حرف":
            c = d = random.choices(a)
            d = random.choices(b)
            f = [c[0], c[0], c[0], c[0], c[0], d[0]]
            random.shuffle(f)
            username = ''.join(f)
        elif choice == 8: # or choice == "سداسي_حرفين":
            c = d = random.choices(a)
            d = random.choices(b)
            f = [c[0], d[0], c[0], d[0], c[0], d[0]]
            random.shuffle(f)
            username = ''.join(f)
        elif choice == 9: # or choice == "شبه_سداسي_ارقام_2":
            c = random.choices(b)
            s = random.choices(e)
            d = random.choices(e)
            f = [s[0], d[0], c[0], c[0], c[0], c[0]]
            username = ''.join(f)
        elif choice == 10: # or choice == "شبه_خماسي_1":
            c = random.choices(e)
            s = random.choices(e)
            d = random.choices(e)
            f = [c[0], c[0], c[0], s[0], d[0]]
            username = ''.join(f)
        elif choice == 11: # or choice == "شبه_خماسي_2":
            c = random.choices(e)
            s = random.choices(e)
            d = random.choices(e)
            f = [s[0], d[0], c[0], c[0], c[0]]
            username = ''.join(f)
        elif choice == 12: # or choice == "شبه_خماسي_3":
            c = random.choices(e)
            s = random.choices(e)
            d = random.choices(e)
            f = [c[0], c[0], c[0], s[0], d[0]]
            username = ''.join(f)
        elif choice == 13: # or choice == "رباعي":
            c = random.choices(e)
            d = random.choices(e)
            f = [c[0], d[0], "_", d[0], c[0]]
            random.shuffle(f)
            username = ''.join(f)
        elif choice == 14: # or choice == "بوتات_ثلاثي":
            c = random.choices(e)
            d = random.choices(e)
            s = random.choices(e)
            f = [c[0], d[0], s[0]]
            random.shuffle(f)
            username = ''.join(f) + 'BOT'
        elif choice == 15: # or choice == "رباعي_1_بوتات":
            c = random.choices(e)
            d = random.choices(e)
            f = [c[0], d[0], c[0], c[0]]
            random.shuffle(f)
            username = ''.join(f) + 'BOT'
        elif choice == 16: # or choice == "رباعي_2_بوتات":
            c = random.choices(e)
            d = random.choices(e)
            f = [c[0], d[0], c[0], d[0]]
            random.shuffle(f)
            username = ''.join(f) + 'BOT'
        elif choice == 17: # or choice == "رباعي_شرطه":
            c = d = random.choices(e)
            d = random.choices(e)
            f = [c[0], d[0], c[0], c[0], "_"]
            random.shuffle(f)
            username = ''.join(f)
        elif choice == 18: # or choice == "رباعي_شرطه":
            c = d = random.choices(e)
            d = random.choices(e)
            f = [c[0], d[0], c[0], c[0], "_", c[0], c[0], c[0], c[0], c[0]]
            random.shuffle(f)
            username = ''.join(f)
        
        if username[0] not in b and username[0] != '_' and username[-1] != '_' and '__' not in username:
            return username

# دورة التشغيل الرئيسية للبرنامج
async def main():
    while True:
        await asyncio.sleep(0.01)  # انتظر 0.01 ثانية
        await bot.process_updates() 
        
@bot.callback_query_handler(func=lambda call: call.data == "back")
def edit_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    login = telebot.types.InlineKeyboardButton(text="- اضافة حساب", callback_data="login")
    GETT = telebot.types.InlineKeyboardButton(text="- قسم الجلسات", callback_data="show_menu")
    accounts = telebot.types.InlineKeyboardButton(text="- حساباتك", callback_data="session_files")
    add_user = telebot.types.InlineKeyboardButton(text="- قسم الخاصيه", callback_data="fahs")
    tys_rand = telebot.types.InlineKeyboardButton(text="- الصيد العشوائي", callback_data="random_capture")
    add_file = telebot.types.InlineKeyboardButton(text="- اضف ملف", callback_data="add_files")
    files = telebot.types.InlineKeyboardButton(text="- ملفاتي", callback_data="files")
    check_file = telebot.types.InlineKeyboardButton(text="- فحص ملف", callback_data="check_file")
    dev = telebot.types.InlineKeyboardButton(text="- DEV", url="t.me/GNA_I")
    channel = telebot.types.InlineKeyboardButton(text="- Source", url="t.me/SOURCE_GNAZH")

    markup.add(login, accounts)
    markup.add(GETT)
    markup.add(add_file)
    markup.add(check_file, files)
    markup.add(add_user, tys_rand)
    markup.add(dev, channel)

    bot.edit_message_text("مرحبا بك في سورس جنازه لفحص وصيد اليوزرات 🌊\n\n① بوت فحص وصيد يوزرات 👨‍🔧\n② صيد يوزرات خاصيه 🕵️‍♂️\n③ صيد يوزرات حذف 🗑\n④ صيد عشوائي مفحوص ✅ \n\n⑤ يتم حجز اليوزر المتاح في قناة 🚀", chat_id=message.message.chat.id, message_id=message.message.message_id, reply_markup=markup)

def load_admins():
    if os.path.exists('admins.txt'):
        with open('admins.txt', 'r') as file:
            admins = file.read().splitlines()
            return [int(admin) for admin in admins]
    return []

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id != ADMIN_CHAT_ID:
        return
        
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    ban_user = telebot.types.InlineKeyboardButton(text="حظر مستخدم", callback_data="ban_user")
    unban_user = telebot.types.InlineKeyboardButton(text="إلغاء حظر مستخدم", callback_data="unban_user")
    grant_vip = telebot.types.InlineKeyboardButton(text="السماح لمستخدم", callback_data="grant_vip")
    revoke_vip = telebot.types.InlineKeyboardButton(text="الغاء السماح لمستخدم", callback_data="revoke_vip")
    promote_admin = telebot.types.InlineKeyboardButton(text="رفع ادمن", callback_data="promote_admin")
    demote_admin = telebot.types.InlineKeyboardButton(text="تنزيل ادمن", callback_data="demote_admin")
    markup.add(ban_user, unban_user)
    markup.add(grant_vip, revoke_vip)
    markup.add(promote_admin, demote_admin)
    bot.send_message(message.chat.id, "مرحبا بك في لوحة التحكم الخاصه بسورس جنازه 🌊\n\n• تحكم من الازرار الموجوده بالاسفل ⚡", reply_markup=markup)

admins = load_admins()

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if not is_admin(message.chat.id):
        return
    else:
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        ban_user = telebot.types.InlineKeyboardButton(text="حظر مستخدم", callback_data="ban_user")
        unban_user = telebot.types.InlineKeyboardButton(text="إلغاء حظر مستخدم", callback_data="unban_user")
        grant_vip = telebot.types.InlineKeyboardButton(text="منح اشتراك VIP", callback_data="grant_vip")
        revoke_vip = telebot.types.InlineKeyboardButton(text="إلغاء اشتراك VIP", callback_data="revoke_vip")
        promote_admin = telebot.types.InlineKeyboardButton(text="رفع ادمن", callback_data="promote_admin")
        demote_admin = telebot.types.InlineKeyboardButton(text="تنزيل ادمن", callback_data="demote_admin")
        markup.add(ban_user, unban_user)
        markup.add(grant_vip, revoke_vip)
        markup.add(promote_admin, demote_admin)
        bot.send_message(message.chat.id, "مرحبا بك في لوحة التحكم الخاصه بسورس جنازه 🌊\n\n• تحكم من الازرار الموجوده بالاسفل ⚡", reply_markup=markup)
    

@bot.callback_query_handler(func=lambda call: call.data == "ban_user")
def handle_ban_user(call):
    msg = bot.send_message(call.message.chat.id, "أرسل ايدي المستخدم لحظره من استخدام البوت")
    bot.register_next_step_handler(msg, process_ban_user)

def process_ban_user(message):
    user_id = message.text
    add_banned(user_id)
    bot.send_message(message.chat.id, f"تم حظر المستخدم من البوت 🚫\n\n• ايديه : {user_id}")

@bot.callback_query_handler(func=lambda call: call.data == "unban_user")
def handle_unban_user(call):
    msg = bot.send_message(call.message.chat.id, "أرسل ايدي المستخدم لإلغاء حظره")
    bot.register_next_step_handler(msg, process_unban_user)

def process_unban_user(message):
    user_id = message.text
    remove_banned(user_id)
    bot.send_message(message.chat.id, f"تم إلغاء حظر المستخدم من البوت ✅\n\n• ايديه :{user_id}")

@bot.callback_query_handler(func=lambda call: call.data == "grant_vip")
def handle_grant_vip(call):
    msg = bot.send_message(call.message.chat.id, "أرسل ايدي المستخدم لمنحه اشتراك VIP")
    bot.register_next_step_handler(msg, process_grant_vip)

def process_grant_vip(message):
    user_id = message.text
    add_vip(user_id)
    bot.send_message(message.chat.id, f"تم منح المستخدم اشتراك VIP بنجاح ✅\n\n• ايديه : {user_id}")

@bot.callback_query_handler(func=lambda call: call.data == "revoke_vip")
def handle_revoke_vip(call):
    msg = bot.send_message(call.message.chat.id, "أرسل معرف المستخدم لإلغاء اشتراك VIP")
    bot.register_next_step_handler(msg, process_revoke_vip)

def process_revoke_vip(message):
    user_id = message.text
    remove_vip(user_id)
    bot.send_message(message.chat.id, f"تم إلغاء اشتراك VIP للمستخدم بنجاح \n\n• ايديه : {user_id}")

@bot.callback_query_handler(func=lambda call: call.data == "promote_admin")
def handle_promote_admin(call):
    msg = bot.send_message(call.message.chat.id, "أرسل ايدي المستخدم لرفعه إلى أدمن")
    bot.register_next_step_handler(msg, process_promote_admin)

def process_promote_admin(message):
    user_id = message.text
    add_admin(user_id)
    bot.send_message(message.chat.id, f"تم رفع المستخدم الى ادمن في البوت 👨‍✈️\n\n• ايديه : {user_id}")

@bot.callback_query_handler(func=lambda call: call.data == "demote_admin")
def handle_demote_admin(call):
    msg = bot.send_message(call.message.chat.id, "أرسل ايدي المستخدم لتنزيله إلى من الادمن")
    bot.register_next_step_handler(msg, process_demote_admin)

def process_demote_admin(message):
    user_id = message.text
    remove_admin(user_id)
    bot.send_message(message.chat.id, f"تم تنزيل المستخدم من رتبة ادمن في البوت ⚡\n\n• ايديه : {user_id}")
                
@bot.callback_query_handler(func=lambda call: call.data == "files")
def handle_inline_button(call):
    markup = telebot.types.InlineKeyboardMarkup()
    user_files = [file for file in data["files"] if file["user_id"] == call.from_user.id]

    if not user_files:
        bot.send_message(call.message.chat.id, "لا توجد ملفات مسجلة لك في البوت ❌.")
        return
    
    for i in range(0, len(user_files), 2):
        file_buttons = []
        for j in range(2):
            if i + j < len(user_files):
                file_buttons.append(telebot.types.InlineKeyboardButton(
                    text=user_files[i + j]["filename"], callback_data=f"file_{i + j}"))
        markup.add(*file_buttons)

    bot.send_message(call.message.chat.id, "مرحبا بك عزيزي المستخدم\n• هذه هي ملفاتك في بوت فحص سورس جنازه 🌊\n• اضغط على الزر الخاص بالملف للتحكم به", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("file_"))
def handle_file(call):
        parts = call.data.split('_')
        file_index = parts[1]
        if file_index == 'check':
            file_index = int(parts[2])
        else:
            file_index = int(parts[1])
        user_files = [file for file in data["files"] if file["user_id"] == call.from_user.id]
        if file_index < len(user_files):
            file_info = user_files[file_index]
            markup = telebot.types.InlineKeyboardMarkup()
            if file_info["checking"]:
                stop_check_button = telebot.types.InlineKeyboardButton(text="ايقاف الفحص 🔴", callback_data=f"stop_check_{file_index}")
                markup.add(stop_check_button)
            else:
                start_check_button = telebot.types.InlineKeyboardButton(text="تشغيل الفحص 🟢", callback_data=f"start_check_{file_index}")
                markup.add(start_check_button)
            
            delete_file_button = telebot.types.InlineKeyboardButton(text="حذف الملف 🗑", callback_data=f"delete_file_{file_index}")
            back_button = telebot.types.InlineKeyboardButton(text="رجـــوع 🔙", callback_data="back")
            markup.add(delete_file_button)
            markup.add(back_button)
            
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"تحكم في ملف {file_info['filename']} من الزرار الموجوده بالاسفل ↙️", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, "خطأ في استرجاع معلومات الملف 858.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("start_check_"))
def start_check(call):
    parts = call.data.split('_')
    if len(parts) == 3 and parts[2].isdigit():
        file_index = int(parts[2])
        user_files = [file for file in data["files"] if file["user_id"] == call.from_user.id]
        if user_files and file_index < len(user_files):
            data["files"][file_index]["checking"] = True
            save_data()
            bot.answer_callback_query(call.id, "تم تشغيل الفحص على الملف 🟢")
            bot.register_next_step_handler(call.message, lambda message: process_file(message, file_index))
            handle_file(call)
        else:
            bot.send_message(call.message.chat.id, "خطأ في تشغيل الفحص على الملف.")
    else:
        raise ValueError("Invalid data format for start_check")

@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_check_"))
def stop_check(call):
    parts = call.data.split('_')
    if len(parts) == 3 and parts[2].isdigit():
        file_index = int(parts[2])
        user_files = [file for file in data["files"] if file["user_id"] == call.from_user.id]
        if user_files and file_index < len(user_files):
            data["files"][file_index]["checking"] = False
            save_data()
            bot.answer_callback_query(call.id, "تم ايقاف الفحص على الملف")
            handle_file(call)
        else:
            bot.send_message(call.message.chat.id, "خطأ في ايقاف الفحص على الملف.")
    else:
        raise ValueError("Invalid data format for stop_check")


@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_file_"))
def delete_file(call):
    file_index = int(call.data.split('_')[2])
    user_files = [file for file in data["files"] if file["user_id"] == call.from_user.id]
    file_info = user_files[file_index]

    # حذف الملف من النظام
    user_file_path = os.path.join(USERS_DIRECTORY, f'{call.from_user.id}_file_{file_info["filename"]}')
    if os.path.exists(user_file_path):
        os.remove(user_file_path)

    # حذف الملف من البيانات
    data["files"].remove(file_info)
    save_data()

    bot.send_message(call.message.chat.id, f"تم حذف الملف {file_info['filename']} بنجاح 🗑")
    handle_inline_button(call)


def process_file(message, file_index):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    user_id = message.from_user.id
    sessions = get_session_files(user_id)
    tasks = []
    if file_index == None:
        if message.document:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            users = downloaded_file.decode('utf-8').strip().split('\n')
            for session in sessions:
                task = asyncio.ensure_future(check_usernames(users, session, message.chat.id, None))
                tasks.append(task)
        else:
            bot.send_message(message.chat.id, "ادعم ملفات .txt فقط ⚠️.")
    else:
        user_files = [file for file in data["files"] if file["user_id"] == message.chat.id]
        if file_index < len(user_files):
            file_info = user_files[file_index]
            usernames = file_info['usernames']
            
            for session in sessions:
                task = asyncio.ensure_future(check_usernames(usernames, session, message.chat.id, file_index))
                tasks.append(task)
    loop.run_until_complete(asyncio.gather(*tasks))
            
            
async def check_usernames(users, session, chat_id, file_index):
    if file_index == None:
        file_path = os.path.join(USERNAMES_DIRECTORY, f'{chat_id}.json')
        async with TelegramClient(StringSession(session['session']), API_ID, API_HASH) as client:
            while True:
                channel_id = None
                if not users:
                    bot.send_message(chat_id, f"انتهى فحص جميع اليوزرات بنجاح ✅")
                    break
                for username in users:
                    if not users:
                        bot.send_message(chat_id, f"انتهى فحص جميع اليوزرات بنجاح ✅")
                        break
                    username = username.strip()
                    isav = check_user(username)
                    if "Available" in isav:
                        if channel_id is None:
                            channel_id = await create_channel(client)
                            if channel_id is None:
                                bot.send_message(chat_id, "Failed to create channel.")
                                return

                        try:
                            await client(functions.channels.UpdateUsernameRequest(
                                channel=channel_id,
                                username=username
                            ))
                            now = datetime.now()
                            current_time = now.strftime("%H:%M")
                            bot.send_message(chat_id, f"تم صيد يوزر متاح ✅\n\n• اليوزر : @{username} \n• الوقت : {current_time}\n\nوتم حجزه في قناة اضغط على اليوزر لزيارتها 🚀")
                            bot.send_message(ADMIN_CHAT_ID, f"قام مشترك بصيد يوزر عشوائي 🔀\n\n• اليوزر : @{username} \n• وقت الصيد : {current_time}\n\nوتم حجزه في قناة اضغط على اليوزر لزيارتها 🚀")
                            if os.path.exists(file_path):
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    users = json.load(f)
                                if username in users:
                                    users.remove(username)
                                    with open(file_path, 'w', encoding='utf-8') as f:
                                        json.dump(users, f, ensure_ascii=False, indent=4)

                            channel_id = None
                            break
                        except errors.ChannelsAdminPublicTooMuchError:
                            bot.send_message(chat_id, f"خطأ بصيد اليوزر @{username} \n\n السبب : \n أنت مسؤول في عدد كبير جدًا من القنوات العامة. يرجى جعل بعض القنوات خاصة لتغيير اسم المستخدم لهذه القناة.")
                            if os.path.exists(file_path):
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    users = json.load(f)
                                if username in users:
                                    users.remove(username)
                                    with open(file_path, 'w', encoding='utf-8') as f:
                                        json.dump(users, f, ensure_ascii=False, indent=4)
                            break
                        except errors.FloodWaitError as e:
                            bot.send_message(chat_id, f"حساب الفحص مبند لمدة {e.seconds} ثانية.")
                            await asyncio.sleep(e.seconds)
                        except errors.rpcerrorlist.UsernameInvalidError:
                            pass
                        except Exception as e:
                            pass
    else:
        async with TelegramClient(StringSession(session['session']), API_ID, API_HASH) as client:
            while True:
                channel_id = None
                if not users:
                    bot.send_message(chat_id, f"انتهى فحص جميع اليوزرات بنجاح ✅")
                    break
                for username in users:
                    if not users:
                        bot.send_message(chat_id, f"انتهى فحص جميع اليوزرات بنجاح ✅")
                        break
                    isav = check_user(username)
                    if "Available" in isav:
                        if channel_id is None:
                            channel_id = await create_channel(client)
                            if channel_id is None:
                                bot.send_message(chat_id, "Failed to create channel.")
                                return

                        try:
                            await client(functions.channels.UpdateUsernameRequest(
                                channel=channel_id,
                                username=username
                            ))
                            now = datetime.now()
                            current_time = now.strftime("%H:%M")
                            bot.send_message(chat_id, f"تم صيد يوزر متاح ✅\n\n• اليوزر : @{username} \n• الوقت : {current_time}\n\nوتم حجزه في قناة اضغط على اليوزر لزيارتها 🚀")
                            bot.send_message(ADMIN_CHAT_ID, f"قام مشترك بصيد يوزر عشوائي 🔀\n\n• اليوزر : @{username} \n• وقت الصيد : {current_time}\n\nوتم حجزه في قناة اضغط على اليوزر لزيارتها 🚀")
                            
                            data["files"][file_index]["usernames"].remove(username)
                            save_data()
                            user_files = [file for file in data["files"] if file["user_id"] == chat_id]
                            file_info = user_files[file_index]
                            users = file_info['usernames']

                            channel_id = None
                            break
                        except errors.ChannelsAdminPublicTooMuchError:
                            bot.send_message(chat_id, f"خطأ بصيد اليوزر @{username} \n\n السبب : \n أنت مسؤول في عدد كبير جدًا من القنوات العامة. يرجى جعل بعض القنوات خاصة لتغيير اسم المستخدم لهذه القناة.")
                            data["files"][file_index]["usernames"].remove(username)
                            save_data()
                            user_files = [file for file in data["files"] if file["user_id"] == chat_id]
                            file_info = user_files[file_index]
                            users = file_info['usernames']
                            channel_id = channel_id
                            break
                        except errors.FloodWaitError as e:
                            bot.send_message(chat_id, f"حساب الفحص مبند لمدة {e.seconds} ثانية.")
                            await asyncio.sleep(e.seconds)
                        except errors.rpcerrorlist.UsernameInvalidError:
                            pass
                        except Exception as e:
                            pass


def get_session_files(user_id):
    file_path = os.path.join(user_session_folder, f"{user_id}.json")
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        sessions = json.load(f)
    return sessions

@bot.callback_query_handler(func=lambda call: call.data == "session_files")
def show_session_files(call):
    user_id = call.from_user.id
    session_files = get_session_files(user_id)

    if not session_files:
        bot.send_message(call.message.chat.id, "لا يوجد جلسات مسجلة لك في البوت ❌.")
        return

    markup = types.InlineKeyboardMarkup()
    for session in session_files:
        phone_number = session['phone_number']
        session_button = types.InlineKeyboardButton(text=phone_number, callback_data=f"session_{phone_number}")
        markup.add(session_button)

    back_button = types.InlineKeyboardButton(text="رجـــوع 🔙", callback_data="back")
    markup.add(back_button)
    bot.edit_message_text("اختر جلسة الرقم الذي تريد التحكم فيه عن طريق الضغط على الزر الخاص بالرقم 🌊", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("session_"))
def manage_session(call):
    user_id = call.from_user.id
    phone_number = call.data.split("_")[1]
    session_files = get_session_files(user_id)

    for session in session_files:
        if session['phone_number'] == phone_number:
            markup = telebot.types.InlineKeyboardMarkup()
            delete_button = telebot.types.InlineKeyboardButton(text="حذف الرقم", callback_data=f"delete_{phone_number}")
            back_button = telebot.types.InlineKeyboardButton(text="رجـــوع 🔙", callback_data="session_files")
            markup.add(delete_button, back_button)
            bot.edit_message_text(f"إدارة الجلسة : {phone_number}\n\n- التحقق بخطوتين : {session['two-step']}\n\n- الجلسة : `{session['session']}`", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
            return

    bot.send_message(call.message.chat.id, "لم يتم العثور على هذه الجلسة ⚠️.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_"))
def delete_session(call):
    user_id = call.from_user.id
    phone_number = call.data.split("_")[1]
    file_path = os.path.join(user_session_folder, f"{user_id}.json")

    if not os.path.exists(file_path):
        bot.send_message(call.message.chat.id, "هذه الجلسة محذوفة بالفعل ⚠️.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        sessions = json.load(f)

    sessions = [session for session in sessions if session['phone_number'] != phone_number]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sessions, f, ensure_ascii=False, indent=4)

    bot.send_message(call.message.chat.id, f"تم حذف الرقم وانهاء جلسته من البوت 🗑")
    show_session_files(call)


 
if __name__ == "__main__":
    bot.polling()
import telebot
from telebot import types
import time
import threading
import smtplib
from email.mime.text import MIMEText
import os
from colorama import Fore, init

init()
ADMIN_ID = 7586070015  

bot = telebot.TeleBot("8112815105:AAEh0rwbPhYdjfbfh6Eyofm09mv0taN3JFc") 

USERS_FILE = "user.txt"
SUBS_FILE = "sub.txt"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        pass

if not os.path.exists(SUBS_FILE):
    with open(SUBS_FILE, "w") as f:
        pass

EMAILS_TO = [
    'stopCA@telegram.org', 
    'dmca@telegram.org', 
    'abuse@telegram.org',
    'sticker@telegram.org', 
    'support@telegram.org'
]

EMAILS_FROM = {
       'miranovseverov@gmail.com': ' kdbc vmdb djxf pmiq',
	   'maksimafanacefish@gmail.com': 'hdpn tbfp acwv jyro',
	   'artemkrotisov@gmail.com': 'zglw vgak tfov uxao',
	   'Vanakrotisov@gmail.com': 'gukl qhxy uxea yhil',
	   'leravladimir237@gmail.com': 'ndon fzio vskk bidt ',
	   'suckdick12345222@gmail.com': 'ckcw eqdv nsjv whgm',
	   'alenaveterov@gmail.com': 'hmiq xwmr yfmw prsa',  
	   'linadurov@gmail.com': 'gsbp xyts brbu dlpw',
	   'kolyaivanov000k@gmail.com': 'mfhg eeio ayau zked',
	   "dlatt6677@gmail.com": "usun ruef otzx zcrh",
	   "edittendo0@gmail.com": "mzdl lrmx puyq epur",
	   "shshsbsbsbwbwvw@gmail.com": "jqrx qivo qxjy jejt",
	   "IvanKarma2000@gmail.com": "irlr cggo xksq tlbb",
	   "misha28272727@gmail.com": "kgwqxvkgjyccibkm",
	   "trevorzxasuniga214@gmail.com": "egnr eucw jvxg jatq",
	   "dellapreston50@gmail.com": "qoit huon rzsd eewo",
	   "neilfdhioley765@gmail.com": "rgco uwiy qrdc gvqh",
	   "samuelmnjassey32@gmail.com": "lgct cjiw nufr zxjg",
	   "segapro72@gmail.com": "ubmq pbrt ujqy orhf",
	   "kurokopotok@gmail.com": "pxww ewut uffz ufpu",
	   "kalievutub@gmail.com": "jlwb otxo mppi jvdh",
	   "snosakka07@gmail.com": "yiro khva gafc lujr",
	   "prosega211@gmail.com": "fnrz rkrp nrwy yaig",
	   "qwaerlarp@gmail.com": "zrzx siyf ukvm ctjp",
	   "segatel093@gmail.com": "fsma qetz gvmp pqrm",
	   "irina15815123@gmail.com": "fmre mxne ncaw gnke",
	   "germanalexandrovich12345678@gmail.com": "tsln hvmz mipp kmwh"
}

print(Fore.RED + """
Приветствую тебя дорогой покупатель!
Желаю тебе удачного использования бота!
Coder by: @onion_xanax
""")

def is_subscribed(user_id):
    with open(SUBS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) == 2 and parts[0] == str(user_id):
                return True
    return False

def add_user(user_id):
    with open(USERS_FILE, "r+") as f:
        users = f.readlines()
        if f"{user_id}\n" not in users:
            f.write(f"{user_id}\n")

def count_users():
    with open(USERS_FILE, "r") as f:
        return len(f.readlines())

def count_vip_users():
    with open(SUBS_FILE, "r") as f:
        return len(f.readlines())

def send_email(subject, body, email_from, password):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = ", ".join(EMAILS_TO)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(email_from, password)
            smtp_server.sendmail(email_from, EMAILS_TO, msg.as_string())
        return True
    except Exception as e:
        print(f"Ошибка отправки письма: {e}")
        return False

def send_complaints(username, user_id, complaint_type, chat_id):
    messages = {
        "spam": f"""Уважаемая администрация Telegram,

Прошу вас принять меры в отношении аккаунта {username} [{user_id}] за рассылку спама. Пользователь массово отправляет рекламные и навязчивые сообщения, что нарушает правила платформы.

Прошу проверить данный аккаунт и при необходимости ограничить его деятельность.

Спасибо за внимание.""",
        "porn": f"""Уважаемая служба поддержки Telegram,

Сообщаю о нарушении со стороны аккаунта {username} [{user_id}], который распространяет порнографический контент. Данные действия противоречат правилам Telegram.

Прошу вас проверить указанный аккаунт и принять соответствующие меры.
Благодарю за понимание.""",
        "terror": f"""Администрации Telegram,

Аккаунт {username} [{user_id}] распространяет материалы, связанные с террористической деятельностью, что является серьёзным нарушением.

Прошу вас срочно проверить данный профиль и заблокировать его в соответствии с политикой платформы.

С уважением.""",
        "personal": f"""Поддержка Telegram,

Аккаунт {username} [{user_id}] публикует личные данные пользователей без их согласия, что является нарушением конфиденциальности.

Прошу вас рассмотреть данную жалобу и принять меры для удаления незаконно размещённой информации.
Заранее благодарен."""
    }

    body = messages.get(complaint_type, "")
    if not body:
        return 0, len(EMAILS_FROM)  
    
    sent = 0
    failed = 0
    
    msg = bot.send_message(chat_id, f"""<pre>
🚀Отправка жалоб начался!

✅Отправлено: {sent}
❌Не отправлено: {failed}
➖➖➖➖➖➖➖➖➖➖
🧖🏼‍♂️Username: {username}
🆔ID: {user_id}
➖➖➖➖➖➖➖➖➖➖
</pre>""", parse_mode="HTML")
    
    for email, password in EMAILS_FROM.items():
        if send_email("Жалоба на нарушение", body, email, password):
            sent += 1
        else:
            failed += 1
        
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=f"""<pre>
🚀Отправка жалоб начался!

✅Отправлено: {sent}
❌Не отправлено: {failed}
➖➖➖➖➖➖➖➖➖➖
🧖🏼‍♂️Username: {username}
🆔ID: {user_id}
➖➖➖➖➖➖➖➖➖➖
</pre>""", parse_mode="HTML")
        except:
            pass
        
        time.sleep(1)
    
    return sent, failed

def send_channel_complaints(channel_link, chat_id):
    body = f"""Уважаемая администрация Telegram,

Прошу вас принять меры в отношении канала {channel_link}, который незаконно распространяет личные данные без согласия соответствующих лиц. Данные действия нарушают условия использования Telegram, а также положения законодательства о защите персональных данных.

Прошу провести проверку указанного канала, удалить конфиденциальную информацию и при необходимости применить санкции вплоть до блокировки."""
    
    sent = 0
    failed = 0
    
    msg = bot.send_message(chat_id, f"""<pre>
🚀Отправка жалоб начался!

✅Отправлено: {sent}
❌Не отправлено: {failed}
➖➖➖➖➖➖➖➖➖➖
🔍Канал: {channel_link}
➖➖➖➖➖➖➖➖➖➖
</pre>""", parse_mode="HTML")
    
    for email, password in EMAILS_FROM.items():
        if send_email("Жалоба на канал", body, email, password):
            sent += 1
        else:
            failed += 1
        
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=f"""<pre>
🚀Отправка жалоб начался!

✅Отправлено: {sent}
❌Не отправлено: {failed}
➖➖➖➖➖➖➖➖➖➖
🔍Канал: {channel_link}
➖➖➖➖➖➖➖➖➖➖
</pre>""", parse_mode="HTML")
        except:
            pass
        
        time.sleep(1)
    
    return sent, failed

@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.from_user.id)
    
    markup = types.InlineKeyboardMarkup()
    
    btn1 = types.InlineKeyboardButton("💣Снос аккаунта", callback_data="account_ban")
    btn2 = types.InlineKeyboardButton("💣Снос канала", callback_data="channel_ban")
    btn3 = types.InlineKeyboardButton("📜Найти нарушение", url="https://t.me/funstat_fanbot?start=0101C2A48F1A00000000")
    btn4 = types.InlineKeyboardButton("🆔Аккаунт", callback_data="account_info")
    btn5 = types.InlineKeyboardButton("💳Подписка", callback_data="subscription")
    btn6 = types.InlineKeyboardButton("💻Модерация", url="t.me/BOG_OSINTEPOB")
    
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5, btn6)
    
    if message.from_user.id == ADMIN_ID:
        btn7 = types.InlineKeyboardButton("🏝Админ панель", callback_data="admin_panel")
        markup.row(btn7)
    
    bot.send_message(message.chat.id, """<pre>
♨️Vishenka -  Snoser,  это ботнет - сносер способный за считанные секунды,
      стереть аккаунт или же канал с лица Telegram!

💻Owner: @qqvishenka
🏝Channel: https://t.me/+LE1yoZOmpXZkZDVi

🤖Функции бота:
✅Многопоточная отправка жалоб!
✅Отзывчивая модерация!
✅Моментальный снос!

</pre>""", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "account_ban")
def account_ban(call):
    if not is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "❌Ваша подписка не активна!", show_alert=True)
        return
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🚮Спам", callback_data="complaint_spam")
    btn2 = types.InlineKeyboardButton("🔞Порнография", callback_data="complaint_porn")
    btn3 = types.InlineKeyboardButton("🏴‍☠️Терроризм", callback_data="complaint_terror")
    btn4 = types.InlineKeyboardButton("📇Личная информация", callback_data="complaint_personal")
    
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                         text="Выберите тип жалобы:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("complaint_"))
def complaint_type(call):
    complaint_type = call.data.split("_")[1]
    msg = bot.send_message(call.message.chat.id, "Введите @username нарушителя:")
    bot.register_next_step_handler(msg, lambda m: get_user_id_for_complaint(m, complaint_type))

def get_user_id_for_complaint(message, complaint_type):
    username = message.text
    msg = bot.send_message(message.chat.id, "Введите ID нарушителя:")
    bot.register_next_step_handler(msg, lambda m: process_complaint(m, username, complaint_type))

def process_complaint(message, username, complaint_type):
    user_id = message.text
    
    def send_complaints_thread():
        sent, failed = send_complaints(username, user_id, complaint_type, message.chat.id)
        bot.send_message(message.chat.id, f"""<pre>
🚀Жалобы успешно отправлены!

✅Отправлено: {sent}
❌Не отправлено: {failed}
➖➖➖➖➖➖➖➖➖➖
🧖🏼‍♂️Username: {username}
🆔ID: {user_id}
➖➖➖➖➖➖➖➖➖➖
💣Ждите пока жертву поглатят жалобы!
</pre>""", parse_mode="HTML")
    
    thread = threading.Thread(target=send_complaints_thread)
    thread.start()

@bot.callback_query_handler(func=lambda call: call.data == "channel_ban")
def channel_ban(call):
    if not is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "❌Ваша подписка не активна!", show_alert=True)
        return
    
    msg = bot.send_message(call.message.chat.id, "Введите ссылку на канал:")
    bot.register_next_step_handler(msg, process_channel_complaint)

def process_channel_complaint(message):
    channel_link = message.text
    
    def send_channel_complaints_thread():
        sent, failed = send_channel_complaints(channel_link, message.chat.id)
        bot.send_message(message.chat.id, f"""<pre>
🚀Жалобы успешно отправлены!

✅Отправлено: {sent}
❌Не отправлено: {failed}
➖➖➖➖➖➖➖➖➖➖
🔍Канал: {channel_link}
➖➖➖➖➖➖➖➖➖➖
💣Ждите пока канал поглатят жалобы!
</pre>""", parse_mode="HTML")
    
    thread = threading.Thread(target=send_channel_complaints_thread)
    thread.start()

@bot.callback_query_handler(func=lambda call: call.data == "account_info")
def account_info(call):
    sub_status = "✅Активна" if is_subscribed(call.from_user.id) else "❌Не активна"
    users_count = count_users()
    vip_count = count_vip_users()
    
    bot.send_message(call.message.chat.id, f"""<pre>
ID: {call.from_user.id}
Подписка: {sub_status}
Кол-во юзеров: {users_count}
Кол-во VIP юзеров: {vip_count}
</pre>""", parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "subscription")
def subscription(call):
    bot.send_message(call.message.chat.id, """<pre>
Приветствую тебя дорогой пользователь!
Для того что бы купить подписку напишите владельцу бота: @qqvishenka.
Владелец подберет вам самый удобный способ приобретения подписки на данного бота.
</pre>""", parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "admin_panel" and call.from_user.id == ADMIN_ID)
def admin_panel(call):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("✅Выдать подписку", callback_data="give_sub")
    btn2 = types.InlineKeyboardButton("❌Отобрать подписку", callback_data="remove_sub")
    btn3 = types.InlineKeyboardButton("📬Рассылка", callback_data="broadcast")
    
    markup.row(btn1, btn2)
    markup.row(btn3)
    
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                         text="Админ панель:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "give_sub" and call.from_user.id == ADMIN_ID)
def give_sub(call):
    msg = bot.send_message(call.message.chat.id, "Введите ID пользователя:")
    bot.register_next_step_handler(msg, lambda m: get_days_for_sub(m, "give"))

def get_days_for_sub(message, action):
    try:
        user_id = int(message.text)
        if action == "give":
            msg = bot.send_message(message.chat.id, "Введите количество дней:")
            bot.register_next_step_handler(msg, lambda m: add_subscription(m, user_id))
    except ValueError:
        bot.send_message(message.chat.id, "Неверный ID пользователя!")

def add_subscription(message, user_id):
    try:
        days = int(message.text)
        with open(SUBS_FILE, "a") as f:
            f.write(f"{user_id}:{days}\n")
        bot.send_message(message.chat.id, f"Подписка на {days} дней выдана пользователю {user_id}!")
    except ValueError:
        bot.send_message(message.chat.id, "Неверное количество дней!")

@bot.callback_query_handler(func=lambda call: call.data == "remove_sub" and call.from_user.id == ADMIN_ID)
def remove_sub(call):
    msg = bot.send_message(call.message.chat.id, "Введите ID пользователя:")
    bot.register_next_step_handler(msg, process_remove_sub)

def process_remove_sub(message):
    try:
        user_id = int(message.text)
        with open(SUBS_FILE, "r") as f:
            lines = f.readlines()
        
        with open(SUBS_FILE, "w") as f:
            for line in lines:
                if not line.startswith(f"{user_id}:"):
                    f.write(line)
        
        bot.send_message(message.chat.id, f"Подписка пользователя {user_id} отозвана!")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный ID пользователя!")

@bot.callback_query_handler(func=lambda call: call.data == "broadcast" and call.from_user.id == ADMIN_ID)
def broadcast(call):
    msg = bot.send_message(call.message.chat.id, "Введите текст рассылки:")
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    with open(USERS_FILE, "r") as f:
        users = [line.strip() for line in f.readlines()]
    
    for user_id in users:
        try:
            bot.send_message(user_id, message.text)
        except:
            pass
    
    bot.send_message(message.chat.id, f"Рассылка отправлена {len(users)} пользователям!")

bot.polling(none_stop=True)

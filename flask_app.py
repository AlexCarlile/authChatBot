import telebot
import sqlite3
from datetime import datetime
import time
from flask import Flask, g
import re

API_TOKEN = '7225254984:AAGDfpxT5c26-6B3MIFK6liwfHaZq9Rhu68'
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)
DATABASE_USERS = 'users.db'

CHAT_LINKS = {
    'endocrinology_yandex': 'https://t.me/+T5OMwwy6fvw5OTIy',
    'endocrinology_vk': 'https://t.me/+xqHt_wqqvhY3NjAy',
    'endocrinology_whatsapp': 'https://t.me/+pybHj-6rptA3ZGJi',
    'endocrinology_email': 'https://t.me/+a0M1ZI9L56M3OWYy',
    'endocrinology_crosspromo': 'https://t.me/+5wCV5rhvoYxjM2Ey',
    'endocrinology_events': 'https://t.me/+fOezHO1MJwtjNDcy',
    'endocrinology_students': 'https://t.me/+h1fApTxnm641YmUy',
    'peds_yandex': 'https://t.me/+LnGKPdkBg_NhZmIy',
    'peds_vk': 'https://t.me/+8sjCmG-CRi1hOWVi',
    'peds_whatsapp': 'https://t.me/+8ZE4OzGb4rMxMzEy ',
    'peds_email': 'https://t.me/+L_jtbIj0kAVlYzAy ',
    'peds_crosspromo': 'https://t.me/+Tdg9njFsw5FkOWIy',
    'peds_events': 'https://t.me/+YKRia5zzCjs4Y2Zi',
    'peds_students': 'https://t.me/+MHLAVCYLgiYwODMy',
    'gynecology_yandex': 'https://t.me/+GtNLzxuHpdU0Zjhi',
    'gynecology_vk': 'https://t.me/+HNH5etzrPaZlZmVi',
    'gynecology_whatsapp': 'https://t.me/+whZ78FVHAvc5MGEy ',
    'gynecology_email': 'https://t.me/+WDAR9ute4ehjOGYy ',
    'gynecology_crosspromo': 'https://t.me/+0-82xpTps7hlNTUy',
    'gynecology_events': 'https://t.me/+eQuNq1HdEQhjNzVi ',
    'gynecology_students': 'https://t.me/+d9OiypbtW-ViZmEy ',
    'cardiology_yandex': 'https://t.me/+ZLwoMxc0N4FmMWUy',
    'cardiology_vk': 'https://t.me/+HKGeYoDS94c4YzNi ',
    'cardiology_whatsapp': 'https://t.me/+0UrgC0QCv1Q3NTVi ',
    'cardiology_email': 'https://t.me/+eo-D2dVCi9E4YzBi ',
    'cardiology_crosspromo': 'https://t.me/+NrMWd7Wx3iNjOTQy',
    'cardiology_events': 'https://t.me/+58CUalNu8CBlOGRi ',
    'cardiology_students': 'https://t.me/+HAw7bG--gkRmNjBi ',
    'derma_yandex': 'https://t.me/+SH-IoKT0VcxiNGVi',
    'derma_vk': 'https://t.me/+m-v1GyTd_8A2NDYy',
    'derma_whatsapp': 'https://t.me/+iqj_cHtwYixhM2Zi',
    'derma_email': 'https://t.me/+BDmKDvOs3zY0ODZi ',
    'derma_crosspromo': 'https://t.me/+OZ-38pQtqzViMDQy',
    'derma_events': 'https://t.me/+2huCw_nRn5M0NDQy ',
    'derma_students': '',
    'medtouch_yandex': 'https://t.me/+HEtjpyxZ8vpmNTFi',
    'medtouch_vk': 'https://t.me/+we69RhNRQPs3MTBi',
    'medtouch_whatsapp': 'https://t.me/+JGL--DmZKoU4YTU6 ',
    'medtouch_email': 'https://t.me/+czuHSIYZi_40NmE6 ',
    'medtouch_crosspromo': 'https://t.me/+3icB1Lm7kX0yNTgy ',
    'medtouch_events': 'https://t.me/+GMfXuOY1tj9mNTMy ',
    'rzm_events': 'https://t.me/+PyhIbmbqPEU0Zjky',
    'allergology_events': 'https://t.me/+SrtZ0NQyQCRmZmQy',
    'trauma_yandex': 'https://t.me/+cnmmJad5ivo4YTU6',
    'trauma_vk': 'https://t.me/+Iqw84WG7Aww5MjVi ',
    'trauma_whatsapp': 'https://t.me/+Iqw84WG7Aww5MjVi ',
    'trauma_email': 'https://t.me/+XRuOBIpLjtE2YmNi ',
    'trauma_crosspromo': 'https://t.me/+5KcQagQVSw0wNWNi ',
    'trauma_events': 'https://t.me/+DeNQKo9XJhoyZjVi ',
    'trauma_students': 'https://t.me/+CzXIc93VIiRjOTVi ',
    'reuma_yandex': 'https://t.me/+1hNztwB4ExM2ZDAy',
    'reuma_vk': 'https://t.me/+YiAYIJdky8o3MTEy ',
    'reuma_whatsapp': 'https://t.me/+MHGfloBzb502MjNi ',
    'reuma_email': 'https://t.me/+_rTkPMnMipM4MmYy',
    'reuma_crosspromo': 'https://t.me/+ahBpT9zJqTRmMDMy',
    'reuma_events': 'https://t.me/+6OxiVrWGctgxMTdi',
    'nevrology': 'https://t.me/nevrochat',
    'parkinsonology': 'https://t.me/+DzKEd_ygoJ40N2Ey',
    'mammology': 'https://t.me/mammologists_chat',    
    'headneck': 'https://t.me/+b1go7uE4tTE4ZTA6',
    'gastro': 'https://t.me/+Zo0WgMoXKGkyODJi',
    'chemotherapist': 'https://t.me/+nO1wiSqVw0oyODVi',
    'ophthalmology': 'https://t.me/+69N5rr_ql3tjZTAy',
    'hematology': 'https://t.me/+r8P-EF4_0B8wYjU6',
}

def get_db_users():
    db = getattr(g, '_database_users', None)
    if db is None:
        db = sqlite3.connect(DATABASE_USERS)
        g._database_users = db
    return db

@app.teardown_appcontext
def close_db_users(exception):
    db = g.pop('_database_users', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        conn = get_db_users()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                email TEXT,
                username TEXT,
                specialization TEXT,
                channel TEXT,
                registration_date TEXT
            )
        ''')
        conn.commit()
        cursor.close()
        print("Таблица users создана или уже существует.")

def is_user_registered_for_specialization(conn, username, specialization):
    attempts = 5
    for attempt in range(attempts):
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE username = ? AND specialization = ?', (username, specialization))
            result = cursor.fetchone()
            cursor.close()
            print(f"Проверка регистрации для пользователя {username}, специализация {specialization}: {'зарегистрирован' if result else 'не зарегистрирован'}")
            return result is not None
        except sqlite3.OperationalError as e:
            if 'locked' in str(e):
                print("База данных заблокирована. Повторная попытка...")
                time.sleep(0.1)  # Ждем немного перед повтором
            else:
                print(f"Ошибка при проверке регистрации: {e}")
                return False

def copy_user_data_for_new_specialization(username, specialization, channel):
    attempts = 5
    cursor = None
    for attempt in range(attempts):
        try:
            conn = get_db_users()
            cursor = conn.cursor()

            # Получаем данные пользователя
            cursor.execute('SELECT full_name, email FROM users WHERE username = ?', (username,))
            user_data = cursor.fetchone()

            if user_data:
                full_name, email = user_data
                registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Проверяем, зарегистрирован ли пользователь для данной специализации
                cursor.execute('SELECT id FROM users WHERE username = ? AND specialization = ?', (username, specialization))
                result = cursor.fetchone()

                if result:
                    print(f"Пользователь {username} уже зарегистрирован для специализации {specialization}.")
                else:
                    cursor.execute('''
                        INSERT INTO users (full_name, email, username, specialization, channel, registration_date) 
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (full_name, email, username, specialization, channel, registration_date))
                    conn.commit()
                    print(f"Пользователь {username} зарегистрирован для специализации {specialization}.")
            else:
                print(f"Данные пользователя {username} не найдены для копирования.")
            break  # Успех, выходим из цикла
        except sqlite3.OperationalError as e:
            if 'locked' in str(e):
                print("База данных заблокирована. Повторная попытка...")
                time.sleep(0.1)  # Ждем немного перед повтором
            else:
                print(f"Ошибка при копировании данных: {e}")
                raise
        finally:
            if 'cursor' in locals():
                cursor.close()  # Закрываем курсор, только если он был открыт

def save_user(conn, full_name, email, username, specialization, channel):
    registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    attempts = 5  # Увеличиваем количество попыток
    cursor = None
    for attempt in range(attempts):
        try:
            print(f"Попытка сохранить пользователя {username}: {full_name}, {email}, {specialization}, {channel} {registration_date}")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (full_name, email, username, specialization, channel, registration_date) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (full_name, email, username, specialization, channel, registration_date))
            conn.commit()
            cursor.close()
            print(f"Данные пользователя {username} сохранены в базе: {full_name}, {email}, {specialization}, {channel}, {registration_date}.")
            break
        except sqlite3.OperationalError as e:
            if 'locked' in str(e):
                print("База данных заблокирована. Повторная попытка...")
                time.sleep(0.1)
            else:
                print(f"Ошибка при сохранении пользователя: {e}")
                raise
        finally:
            cursor.close()  # Закрываем курсор

def parse_specialization_and_channel(start_param):
    parts = start_param.split('_', 1)
    full_spec = start_param
    specialization = parts[0] if parts else ''
    channel = parts[1] if len(parts) > 1 else 'unknown'
    return full_spec, specialization, channel

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    start_params = message.text.split()
    if len(start_params) > 1:
        full_spec, specialization, channel = parse_specialization_and_channel(start_params[1])
        print('В full_spec: ', full_spec)
        print('В specialization: ', specialization)
        print('В channel: ', channel)
        print(f"full_spec: '{full_spec}'")
        print(f"CHAT_LINKS keys: {list(CHAT_LINKS.keys())}")
        print(f"Check direct match: {full_spec in CHAT_LINKS}")
        if full_spec in CHAT_LINKS:
            username = message.from_user.username
            print(f"Запрос на старт от пользователя {username} со специализацией {specialization}.")

            with app.app_context():  # Создаем контекст приложения
                if is_user_registered_for_specialization(get_db_users(), username, specialization):
                    chat_link = CHAT_LINKS[full_spec]
                    bot.send_message(message.chat.id, f"Вы уже зарегистрированы. Нажмите на ссылку для вступления в чат: {chat_link}")
                else:
                    conn = get_db_users()
                    cursor = conn.cursor()
                    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
                    if cursor.fetchone():
                        copy_user_data_for_new_specialization(username, specialization, channel)
                        chat_link = CHAT_LINKS[full_spec]
                        bot.send_message(message.chat.id, f"Вы зарегистрированы в новом чате. Нажмите на ссылку для вступления: {chat_link}")
                    else:
                        user_data[message.chat.id] = {'specialization': specialization, 'channel': channel}
                        bot.send_message(message.chat.id, "Введите ваше полное имя (ФИО):")
                        bot.register_next_step_handler(message, lambda msg: process_full_name(msg, full_spec))
                    cursor.close()  # Закрываем курсор
        else:
            bot.send_message(message.chat.id, "Указанная специализация не найдена.")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, укажите специализацию в ссылке.")

def process_full_name(message, full_spec):
    full_name = message.text.strip()
    # Регулярное выражение для проверки корректности ФИО
    full_name_pattern = r'^[А-ЯЁ][а-яё]+(?: [А-ЯЁ][а-яё]+){1,2}$'
    
    if re.match(full_name_pattern, full_name):
        user_data[message.chat.id]['full_name'] = full_name
        print(f"Получено корректное полное имя: {full_name}")
        bot.send_message(message.chat.id, "Введите ваш email:")
        bot.register_next_step_handler(message, lambda msg: process_email(msg, full_spec))
    else:
        print(f"Введено некорректное полное имя: {full_name}")
        bot.send_message(message.chat.id, "Некорректный формат ФИО. Пожалуйста, введите полное имя в формате: Фамилия Имя Отчество.")
        bot.register_next_step_handler(message, lambda msg: process_full_name(msg, full_spec))

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def process_email(message, full_spec):
    email = message.text.strip()
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(email_pattern, email):
        user_data[message.chat.id]['email'] = email
        username = message.from_user.username
        specialization = user_data[message.chat.id]['specialization']
        channel = user_data[message.chat.id]['channel']
        full_name = user_data[message.chat.id]['full_name']
        
        print(f"Сохранение пользователя {full_name} с email {email} и специализацией {specialization}.")
        
        with app.app_context():
            conn = get_db_users()  # Получаем соединение с базой данных
            save_user(conn, full_name, email, username, specialization, channel)  # Передаем все необходимые аргументы, включая conn
        
        chat_link = CHAT_LINKS[full_spec]
        bot.send_message(message.chat.id, f"Спасибо! Нажмите на ссылку для вступления в чат: {chat_link}")
    else:
        print(f"Введен некорректный e-mail: {email}")
        bot.send_message(message.chat.id, "Некорректный формат e-mail. Пожалуйста, введите действительный адрес электронной почты:")
        bot.register_next_step_handler(message, process_email)


if __name__ == '__main__':
    init_db()  # Вызываем инициализацию базы данных
    with app.app_context():  # Создаем контекст приложения
        bot.polling()

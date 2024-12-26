import telebot
import sqlite3
from datetime import datetime
import time
from flask import Flask, g
import re

API_TOKEN = '7534027613:AAGiTWuOPEylP2mj3lDFklTPyQ4eoqo3DI4'
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)
DATABASE_USERS = 'users.db'

CHAT_LINKS = {
    'allergology': 'https://t.me/+jEH6AU3C-h85Nzcy',
    'gynecology': 'https://t.me/gynechat',
    'endocrinology': 'https://t.me/+953vhmTg1zswMzI6',
    'peds': 'https://t.me/aibolitmg',
    'rzm': 'https://t.me/+aADYZsheL-ZlZTUy',
    'derma': 'https://t.me/+MT3Bt90nanEwOWMy',
    'nevrology': 'https://t.me/nevrochat',
    'parkinsonology': 'https://t.me/+DzKEd_ygoJ40N2Ey',
    'trauma': 'https://t.me/+Vf0GKyXZJeVmNTMy',
    'mammology': 'https://t.me/mammologists_chat',    
    'headneck': 'https://t.me/+b1go7uE4tTE4ZTA6',
    'medtouch': 'https://t.me/medtouch',
    'gastro': 'https://t.me/+Zo0WgMoXKGkyODJi',
    'reuma': 'https://t.me/+4ZOCmjqDqtUxNzk6',
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

def copy_user_data_for_new_specialization(username, specialization):
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
                        INSERT INTO users (full_name, email, username, specialization, registration_date) 
                        VALUES (?, ?, ?, ?, ?)
                    ''', (full_name, email, username, specialization, registration_date))
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

def save_user(conn, full_name, email, username, specialization):
    registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    attempts = 5  # Увеличиваем количество попыток
    cursor = None
    for attempt in range(attempts):
        try:
            print(f"Попытка сохранить пользователя {username}: {full_name}, {email}, {specialization}, {registration_date}")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (full_name, email, username, specialization, registration_date) 
                VALUES (?, ?, ?, ?, ?)
            ''', (full_name, email, username, specialization, registration_date))
            conn.commit()
            cursor.close()
            print(f"Данные пользователя {username} сохранены в базе: {full_name}, {email}, {specialization}, {registration_date}.")
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



user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    start_params = message.text.split()
    if len(start_params) > 1:
        specialization = start_params[1]
        if specialization in CHAT_LINKS:
            username = message.from_user.username
            print(f"Запрос на старт от пользователя {username} со специализацией {specialization}.")

            with app.app_context():  # Создаем контекст приложения
                if is_user_registered_for_specialization(get_db_users(), username, specialization):
                    chat_link = CHAT_LINKS[specialization]
                    bot.send_message(message.chat.id, f"Вы уже зарегистрированы. Нажмите на ссылку для вступления в чат: {chat_link}")
                else:
                    conn = get_db_users()
                    cursor = conn.cursor()
                    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
                    if cursor.fetchone():
                        copy_user_data_for_new_specialization(username, specialization)
                        chat_link = CHAT_LINKS[specialization]
                        bot.send_message(message.chat.id, f"Вы зарегистрированы в новом чате. Нажмите на ссылку для вступления: {chat_link}")
                    else:
                        user_data[message.chat.id] = {'specialization': specialization}
                        bot.send_message(message.chat.id, "Введите ваше полное имя (ФИО):")
                        bot.register_next_step_handler(message, process_full_name)
                    cursor.close()  # Закрываем курсор
        else:
            bot.send_message(message.chat.id, "Указанная специализация не найдена.")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, укажите специализацию в ссылке.")

def process_full_name(message):
    full_name = message.text.strip()
    # Регулярное выражение для проверки корректности ФИО
    full_name_pattern = r'^[А-ЯЁ][а-яё]+(?: [А-ЯЁ][а-яё]+){1,2}$'
    
    if re.match(full_name_pattern, full_name):
        user_data[message.chat.id]['full_name'] = full_name
        print(f"Получено корректное полное имя: {full_name}")
        bot.send_message(message.chat.id, "Введите ваш email:")
        bot.register_next_step_handler(message, process_email)
    else:
        print(f"Введено некорректное полное имя: {full_name}")
        bot.send_message(message.chat.id, "Некорректный формат ФИО. Пожалуйста, введите полное имя в формате: Фамилия Имя Отчество.")
        bot.register_next_step_handler(message, process_full_name)

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def process_email(message):
    email = message.text.strip()
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(email_pattern, email):
        user_data[message.chat.id]['email'] = email
        username = message.from_user.username
        specialization = user_data[message.chat.id]['specialization']
        full_name = user_data[message.chat.id]['full_name']
        
        print(f"Сохранение пользователя {full_name} с email {email} и специализацией {specialization}.")
        
        with app.app_context():
            conn = get_db_users()  # Получаем соединение с базой данных
            save_user(conn, full_name, email, username, specialization)  # Передаем все необходимые аргументы, включая conn
        
        chat_link = CHAT_LINKS[specialization]
        bot.send_message(message.chat.id, f"Спасибо! Нажмите на ссылку для вступления в чат: {chat_link}")
    else:
        print(f"Введен некорректный e-mail: {email}")
        bot.send_message(message.chat.id, "Некорректный формат e-mail. Пожалуйста, введите действительный адрес электронной почты:")
        bot.register_next_step_handler(message, process_email)


if __name__ == '__main__':
    init_db()  # Вызываем инициализацию базы данных
    with app.app_context():  # Создаем контекст приложения
        bot.polling()

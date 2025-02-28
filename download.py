import sqlite3
from datetime import datetime
from flask import Flask, g, request, send_file, abort
import csv
import os
from flask_app import get_db_users, DATABASE_USERS  # Импортируем функцию из flask_app.py
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

app = Flask(__name__)

# Читаем секретный ключ из .env
SECRET_KEY = os.getenv("SECRET_KEY")

@app.route('/')
def hello_world():
    return 'Hello N Flask!'

@app.route("/download_users", methods=["GET"])
def download_users():
    # Проверяем API-ключ
    api_key = request.headers.get("Authorization")  # Ожидаем "Bearer <TOKEN>"
    
    if not api_key or api_key != f"Bearer {SECRET_KEY}":
        abort(403, "Доступ запрещен")  # Ошибка 403, если ключ неверный
    
    print(f"Используемый путь к БД: {os.path.abspath(DATABASE_USERS)}")
    filename = export_users_to_csv()
    return send_file(filename, as_attachment=True, download_name="users.csv")

def export_users_to_csv():
    conn = get_db_users()
    cursor = conn.cursor()
    
    # Запрашиваем все данные из таблицы users
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    
    # Определяем путь к файлу
    filename = "users_export.csv"
    
    # Открываем файл и записываем данные
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Записываем заголовки
        writer.writerow([desc[0] for desc in cursor.description])
        
        # Записываем данные
        writer.writerows(rows)
    
    cursor.close()
    return filename

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
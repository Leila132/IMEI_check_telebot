import sqlite3

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('my_database.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Создание таблицы
def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT NOT NULL,
        is_active INTEGER DEFAULT 0
    )
    ''')
    conn.commit()

# Вставка данных
def insert_data(conn, telegram_id):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (telegram_id)
    VALUES (?)
    ''', (telegram_id,))
    conn.commit()

#Обновление при пройденной авторизации (1- авторизован, 0 - нет)
def do_active_user(conn, telegram_id):
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE users
    SET is_active = 1
    WHERE telegram_id = ?
    ''', (telegram_id,))
    conn.commit()

def check_user(conn, telegram_id):
    cursor = conn.cursor()
    cursor.execute('SELECT telegram_id FROM users WHERE telegram_id = ?', (telegram_id,))
    row = cursor.fetchall()
    return len(row) > 0

def check_user_auth_status(conn, telegram_id):
    cursor = conn.cursor()
    cursor.execute('SELECT is_active FROM users WHERE telegram_id = ?', (telegram_id,))
    rows = cursor.fetchall()
    a = [list(row) for row in rows]
    return a[0][0]
import sqlite3

def drop_table():
    database = sqlite3.connect('Equations_users_table.db')
    cursor = database.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS users;''')
    database.commit()
    database.close()
# drop_table()

# Функция для создания таблицы пользователей
def create_users_table():
    database = sqlite3.connect('Equations_users_table.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_number INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id BIGINT NOT NULL UNIQUE,
        full_name TEXT,
        screen TEXT,
        quantity INTEGER DEFAULT 0,
        round INTEGER DEFAULT 1,
        nickname TEXT DEFAULT 'Фронтендер'
    );
    ''')
    database.commit()
    database.close()

# create_users_table()

def set_user_info(user_id, full_name, screen):
    database = sqlite3.connect('Equations_users_table.db')
    cursor = database.cursor()
    cursor.execute('''
        INSERT INTO users(user_id, full_name, screen) VALUES
        (?, ?, ?)
        ''', (user_id, full_name, screen))
    database.commit()
    database.close()

def check_users_in_table(user_id, full_name, screen):
    database = sqlite3.connect('Equations_users_table.db')
    cursor = database.cursor()
    cursor.execute(f'''
            SELECT user_number FROM users WHERE user_id={user_id}
            ''')
    user_number = cursor.fetchone()
    if user_number is not None:
        database.close()
    else:
        set_user_info(user_id, full_name, screen)
        check_users_in_table(user_id, full_name, screen)

def get_all_user_id_and_full_name_quantity_round_nick():
    database = sqlite3.connect('Equations_users_table.db')
    cursor = database.cursor()
    cursor.execute(f'''
            SELECT user_id,  full_name, quantity, round, nickname FROM users;
            ''')
    result = cursor.fetchall()
    database.close()
    result_str = "\n".join([f"{x[0]}, {x[1]}, {x[2]}, round:{x[3]}, {x[4]}" for x in result])
    return result_str


def update_user_screen(user_id, screen):
    database = sqlite3.connect('Equations_users_table.db')
    cursor = database.cursor()
    cursor.execute('''
        UPDATE users SET screen = ? WHERE user_id = ?
        ''', (screen, user_id))
    database.commit()
    database.close()


def get_screen_by_user_id(user_id):
    database = sqlite3.connect('Equations_users_table.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT screen FROM users WHERE user_id=?
    ''', (user_id,))
    result = cursor.fetchone()
    database.close()

    if result:
        return result[0]
    else:
        return '375 1280'

def get_round_by_user_id(user_id):
    database = sqlite3.connect('Equations_users_table.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT round FROM users WHERE user_id=?
    ''', (user_id,))
    result = cursor.fetchone()
    database.close()

    if result:
        return result[0]
    else:
        return 1

def get_nickname_by_user_id(user_id):
    database = sqlite3.connect('Equations_users_table.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT nickname FROM users WHERE user_id=?
    ''', (user_id,))
    result = cursor.fetchone()
    database.close()

    if result:
        return result[0]
    else:
        return 'Фронтендер'

def update_quantity(user_id, count=1):
    database = sqlite3.connect('Equations_users_table.db')
    cursor = database.cursor()
    cursor.execute('''
        UPDATE users SET quantity = quantity + ? WHERE user_id = ?
        ''', (count, user_id))
    database.commit()
    database.close()

def update_round(user_id, roundd):
    database = sqlite3.connect('Equations_users_table.db')
    cursor = database.cursor()
    cursor.execute('''
        UPDATE users SET round = ? WHERE user_id = ?
        ''', (roundd, user_id))
    database.commit()
    database.close()

def update_nickname(user_id, nickname):
    database = sqlite3.connect('Equations_users_table.db')
    cursor = database.cursor()
    cursor.execute('''
        UPDATE users SET nickname = ? WHERE user_id = ?
        ''', (nickname, user_id))
    database.commit()
    database.close()

def get_quantity(user_id):
    database = sqlite3.connect('Equations_users_table.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT quantity FROM users WHERE user_id=?
    ''', (user_id,))
    result = cursor.fetchone()
    database.close()

    if result:
        return result[0]
    else:
        return 0

# Добавить пользователей в белый и черный список

def add_user_to_white_list(user_id):
    database = sqlite3.connect('Equations_users_table.db')
    cursor = database.cursor()
    cursor.execute('''
        UPDATE users SET quantity = 0 WHERE user_id = ?
        ''', (user_id,))
    database.commit()
    database.close()










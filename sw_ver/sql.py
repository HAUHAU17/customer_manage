import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('users.db')
c = conn.cursor()

def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  age INTEGER NOT NULL)''')
    conn.commit()

def create_user(name, age):
    c.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
    conn.commit()

def read_users(search_query=None):
    if search_query:
        query = "SELECT * FROM users WHERE"
        params = []
        for field, value in search_query.items():
            if field == "이름":
                query += " name LIKE ? AND"
                params.append(f"%{value}%")
            elif field == "나이":
                query += " age LIKE ? AND"
                params.append(f"%{value}%")
        query = query.rstrip(" AND")  # 끝의 'AND' 제거
        c.execute(query, params)
    else:
        c.execute('SELECT * FROM users')
    return c.fetchall()

def update_user(user_id, name, age):
    c.execute('UPDATE users SET name = ?, age = ? WHERE id = ?', (name, age, user_id))
    conn.commit()

def delete_user(user_id):
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()

def close_connection():
    conn.close()

# 테이블 생성
create_table()
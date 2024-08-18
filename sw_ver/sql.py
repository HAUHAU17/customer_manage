import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('users.db')
c = conn.cursor()

def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birth TEXT,
            year TEXT,
            month TEXT,
            day TEXT,
            age INTEGER NOT NULL,
            email TEXT,
            gender TEXT,
            phone TEXT,
            address TEXT,
            consultation_start DATE,
            consultation_end DATE,
            issue TEXT,
            sessions INTEGER,
            notes TEXT
        )
    ''')
    conn.commit()

def create_user(name, birth, year, month, day, age, email, gender, phone, address, consultation_start, consultation_end, issue, sessions, notes):
    c.execute('''
        INSERT INTO users (
            name, birth, year, month, day, age, email, gender, phone, address, consultation_start, consultation_end, issue, sessions, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, birth, year, month, day, age, email, gender, phone, address, consultation_start, consultation_end, issue, sessions, notes))
    conn.commit()

def build_search_query(search_query):
    if not search_query:
        return "SELECT * FROM users", []

    query = "SELECT * FROM users WHERE "
    conditions = []
    params = []

    field_map = {
        "ID": "user_id",
        "이름": "name",
        "생년월일": "birth",
        "연도": "year",
        "월": "month",
        "일": "day", 
        "나이": "age",
        "메일": "email",
        "성별": "gender",
        "전화번호": "phone",
        "주소": "address",
        "상담시작일": "consultation_start",
        "상담종료일": "consultation_end",
        "호소문제": "issue",
        "회기 수": "sessions",
        "특이사항": "notes"
    }

    for field, value in search_query.items():
        if field in field_map:
            conditions.append(f"{field_map[field]} LIKE ?")
            params.append(f"%{value}%")

    if conditions:
        query += " AND ".join(conditions)
    else:
        query = "SELECT * FROM users"  # 조건이 없을 경우 전체 조회

    return query, params

def read_users(search_query=None):
    query, params = build_search_query(search_query)
    c.execute(query, params)
    return c.fetchall()

def update_user(user_id, name, birth, year, month, day, age, email, gender, phone, address, consultation_start, consultation_end, issue, sessions, notes):
    c.execute('''
        UPDATE users
        SET name = ?, birth = ?, year = ?, month = ?, day = ?, age = ?, email = ?, gender = ?, phone = ?, address = ?, consultation_start = ?, consultation_end = ?, issue = ?, sessions = ?, notes = ?
        WHERE id = ?
    ''', (name, birth, year, month, day, age, email, gender, phone, address, consultation_start, consultation_end, issue, sessions, notes, user_id))
    conn.commit()

def delete_user(user_id):
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()

def close_connection():
    conn.close()

# 테이블 생성
create_table()
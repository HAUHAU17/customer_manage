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
            year INTEGER,
            month INTEGER,
            day INTEGER,
            age INTEGER NOT NULL,
            email TEXT,
            gender TEXT,
            male TEXT,
            female TEXT,
            phone TEXT,
            address TEXT,
            consultation_start TEXT,
            start_year INTEGER,
            start_month INTEGER,
            start_day INTEGER,
            consultation_end TEXT,
            end_year INTEGER,
            end_month INTEGER,
            end_day INTEGER,
            issue TEXT,
            sessions INTEGER,
            notes TEXT
        )
    ''')
    conn.commit()

def create_user(name, birth, year, month, day, age, email, gender, male, female, phone, address, consultation_start, start_year, start_month, start_day, consultation_end, end_year, end_month, end_day, issue, sessions, notes):
    c.execute('''
        INSERT INTO users (
            name, birth, year, month, day, age, email, gender, male, female, phone, address, consultation_start, start_year, start_month, start_day, consultation_end, end_year, end_month, end_day, issue, sessions, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, birth, year, month, day, age, email, gender, male, female, phone, address, consultation_start, start_year, start_month, start_day, consultation_end, end_year, end_month, end_day, issue, sessions, notes))
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
        "년": "year",
        "월": "month",
        "일": "day", 
        "나이": "age",
        "메일": "email",
        "성별": "gender",
        "남자": "male",
        "여자": "female", 
        "전화번호": "phone",
        "주소": "address",
        "상담시작일": "consultation_start",
        "시작연도" : "start_year",
        "시작월" : "start_month",
        "시작일" : "start_day",
        "상담종료일": "consultation_end",
        "종료연도" : "end_year",
        "종료월" : "end_month",
        "종료일" : "end_day",
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

def update_user(user_id, name, birth, year, month, day, age, email, gender, male, female, phone, address, consultation_start, start_year, start_month, start_day, consultation_end, end_year, end_month, end_day, issue, sessions, notes):
    c.execute('''
        UPDATE users
        SET name = ?, birth = ?, year = ?, month = ?, day = ?, age = ?, email = ?, gender = ?, male = ?, female = ?, phone = ?, address = ?, consultation_start = ?, start_year = ?, start_month = ?, start_day = ?, consultation_end = ?, end_year = ?, end_month = ?, end_day = ?, issue = ?, sessions = ?, notes = ?
        WHERE id = ?
    ''', (name, birth, year, month, day, age, email, gender, male, female, phone, address, consultation_start, start_year, start_month, start_day, consultation_end, end_year, end_month, end_day, issue, sessions, notes, user_id))
    conn.commit()

def delete_user(user_id):
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()

def fetch_users():
    """모든 고객 데이터를 가져오는 함수"""
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, birth, age, email, gender, phone, address, consultation_start, consultation_end, sessions FROM users")  # 'users'는 데이터베이스 테이블 이름
    rows = cursor.fetchall()
    return rows

def fetch_users_by_id(user_id):
    """주어진 사용자 ID에 해당하는 사용자 데이터를 가져오는 함수"""
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, birth, age, email, gender, phone, address, consultation_start, consultation_end, issue, sessions, notes FROM users WHERE id = ?", (user_id,))
    rows = cursor.fetchall()
    return rows

def fetch_user_name_by_id(user_id):
    """주어진 사용자 ID로 사용자 이름을 가져오는 함수"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()  # fetchone()은 하나의 행을 반환
    if result:
        return result[0]  # 첫 번째 열 (이름) 반환
    else:
        return None

def close_connection():
    conn.close()

# 테이블 생성
create_table()
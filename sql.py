import sqlite3

# 데이터베이스 연결 생성 (SQLite는 파일로 데이터베이스를 관리)
conn = sqlite3.connect('customer_management.db')

# 커서 객체 생성
cursor = conn.cursor()

# 고객 정보를 저장할 테이블 생성 (이미 존재하면 생성하지 않음)
cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  email TEXT NOT NULL,
                  address TEXT NOT NULL)''')

conn.commit()

def add_customer(name, birth_year, birth_month, birth_day, age, phone, email, address, gender,
                 session_start_date, session_end_date, presenting_problem, session_count, special_notes):
    # 고객 추가 로직 구현
    # 예를 들어, 데이터베이스에 추가하는 코드
    cursor.execute("""
        INSERT INTO customers (name, birth_year, birth_month, birth_day, age, phone, email, address, gender,
                               session_start_date, session_end_date, presenting_problem, session_count, special_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, birth_year, birth_month, birth_day, age, phone, email, address, gender,
          session_start_date, session_end_date, presenting_problem, session_count, special_notes))
    conn.commit()

def get_customers(query=""):
    query = f"%{query}%"
    cursor.execute("SELECT * FROM customers WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR address LIKE ?", (query, query, query, query))
    return cursor.fetchall()

def delete_customer(customer_id):
    cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
    conn.commit()

def update_customer(customer_id, name, phone, email, address):
    cursor.execute("UPDATE customers SET name=?, phone=?, email=?, address=? WHERE id=?", (name, phone, email, address, customer_id))
    conn.commit()

def get_customer_by_id(customer_id):
    query = """SELECT name, phone, email, address, gender, session_start_date, 
                      session_end_date, presenting_problem, session_count, special_notes
               FROM customers WHERE id = ?"""
    try:
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        if result:
            return result  # (name, phone, email, address, gender, session_start_date, session_end_date, presenting_problem, session_count, special_notes)
        else:
            print(f"No customer found with ID: {customer_id}")  # 디버깅 출력
            return None
    except Exception as e:
        print(f"Error retrieving customer info: {e}")  # 오류 출력
        return None


def get_customer_id_by_info(name, phone, email, address):
    print(f"Searching for: Name='{name}', Phone='{phone}', Email='{email}', Address='{address}'")  # 디버깅 출력
    cursor.execute("SELECT id FROM customers WHERE name=? AND phone=? AND email=? AND address=?", (name, phone, email, address))
    result = cursor.fetchone()
    if result:
        print(f"Found ID: {result[0]}")  # 디버깅 출력
        return result[0]
    print("No matching customer found.")  # 디버깅 출력
    return None

def show_all_customers():
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    for customer in customers:
        print(customer)

def close_connection():
    conn.close()

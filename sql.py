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

def add_customer(name, phone, email, address):
    cursor.execute("INSERT INTO customers (name, phone, email, address) VALUES (?, ?, ?, ?)", (name, phone, email, address))
    conn.commit()
    print(f"Customer added: Name='{name}', Phone='{phone}', Email='{email}', Address='{address}'")  # 디버깅 출력

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
    cursor.execute("SELECT name, phone, email, address FROM customers WHERE id=?", (customer_id,))
    return cursor.fetchone()

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

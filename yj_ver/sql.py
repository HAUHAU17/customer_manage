import sqlite3
from datetime import datetime
import tkinter as tk

# 데이터베이스 연결 생성 (SQLite는 파일로 데이터베이스를 관리)
conn = sqlite3.connect('customer_management.db')

# 커서 객체 생성
cursor = conn.cursor()

# 고객 정보를 저장할 테이블 생성 (이미 존재하면 생성하지 않음)
cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  birth_year INTEGER NOT NULL,
                  birth_month INTEGER NOT NULL,
                  birth_day INTEGER NOT NULL,
                  age INTEGER NOT NULL,
                  phone TEXT NOT NULL,
                  email TEXT NOT NULL,
                  address TEXT NOT NULL,
                  gender TEXT,
                  session_start_date TEXT,
                  session_end_date TEXT,
                  presenting_problem TEXT,
                  session_count INTEGER,
                  special_notes TEXT)''')

conn.commit()

def load_customers(treeview_customers, get_customers, query=""):
    customers = get_customers(query)
    treeview_customers.delete(*treeview_customers.get_children())
    
    for customer in customers:
        # Extract values from customer tuple, handle missing values
        id = customer[0]
        name = customer[1]
        birth_year = customer[2] if customer[2] else "0000"
        birth_month = f"{int(customer[3]):02d}" if customer[3] else "00"
        birth_day = f"{int(customer[4]):02d}" if customer[4] else "00"
        age = customer[5] if customer[5] else ""
        phone = customer[6] if customer[6] else ""
        email = customer[7] if customer[7] else ""
        address = customer[8] if customer[8] else ""
        gender = customer[9] if customer[9] else ""
        session_start_date = customer[10] if customer[10] else ""
        session_end_date = customer[11] if customer[11] else ""
        session_count = customer[13] if customer[13] else "" 

        birthdate = f"{birth_year}-{birth_month}-{birth_day}"
        
        treeview_customers.insert('', tk.END, values=(id, name, birthdate, age, phone, email, address, gender,
                                                      session_start_date, session_end_date, session_count))  



def add_customer(name, birth_year, birth_month, birth_day, age, phone, email, address, gender,
                 session_start_date, session_end_date, presenting_problem, session_count, special_notes):
    # 고객 추가 로직 구현
    cursor.execute("""
        INSERT INTO customers (name, birth_year, birth_month, birth_day, age, phone, email, address, gender,
                               session_start_date, session_end_date, presenting_problem, session_count, special_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, birth_year, birth_month, birth_day, age, phone, email, address, gender,
          session_start_date, session_end_date, presenting_problem, session_count, special_notes))
    conn.commit()

def get_customers(query=""):
    query = f"%{query}%"
    cursor.execute("""
        SELECT id, name, birth_year, birth_month, birth_day, age, phone, email, address, gender,
               session_start_date, session_end_date, presenting_problem, session_count, special_notes
        FROM customers
        WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR address LIKE ?
    """, (query, query, query, query))
    return cursor.fetchall()

def delete_customer(customer_id):
    cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
    conn.commit()

def update_customer(customer_id, updated_name, updated_phone, updated_email, updated_address,
                    updated_gender, updated_birth_year, updated_birth_month, updated_birth_day,
                    updated_age, updated_session_start, updated_session_end,
                    updated_presenting_problem, updated_session_count, updated_special_notes):
    cursor.execute("""
        UPDATE customers
        SET name=?, birth_year=?, birth_month=?, birth_day=?, age=?, phone=?, email=?, address=?, gender=?, 
            session_start_date=?, session_end_date=?, presenting_problem=?, session_count=?, special_notes=?
        WHERE id=?
    """, (updated_name, updated_birth_year, updated_birth_month, updated_birth_day, updated_age,
        updated_phone, updated_email, updated_address, updated_gender,
        updated_session_start, updated_session_end, updated_presenting_problem, 
        updated_session_count, updated_special_notes, customer_id))
    conn.commit()


def get_customer_by_id(customer_id):
    query = """SELECT id, name, birth_year, birth_month, birth_day, age, phone, email, address, gender,
                      session_start_date, session_end_date, presenting_problem, session_count, special_notes
               FROM customers WHERE id = ?"""
    try:
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        if result:
            return result  # (id, name, birth_year, birth_month, birth_day, age, phone, email, address, gender, session_start_date, session_end_date, presenting_problem, session_count, special_notes)
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

def validate_birthdate(year, month, day):
    try:
        if not year and not month and not day:
            return True
        # 연도 검사
        birth_year = int(year)
        if birth_year < 1950 or birth_year > 2050 or birth_year == '0000':
            return False

        # 월 검사
        birth_month = int(month)
        if birth_month < 1 or birth_month > 12 or birth_month == '00':
            return False

        # 일 검사 (월별로 일수 체크)
        birth_day = int(day)
        if birth_day < 1 or birth_day > 31 or birth_day == '00':
            return False
        if birth_month in [4, 6, 9, 11] and birth_day > 30:  # 30일까지만 있는 달
            return False
        if birth_month == 2:  # 윤년 계산 포함
            if (birth_year % 4 == 0 and birth_year % 100 != 0) or (birth_year % 400 == 0):
                if birth_day > 29:
                    return False
            else:
                if birth_day > 28:
                    return False

        return True
    except ValueError:
        return False
    

def close_connection():
    conn.close()

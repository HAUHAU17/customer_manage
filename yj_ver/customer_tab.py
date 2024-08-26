import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
from sql import update_customer, delete_customer, validate_birthdate, load_customers, get_customers, get_customer_by_id

import sqlite3

def create_customer_window(customer_id, treeview_customers):
    """고객 ID로 새 창을 열고 정보를 표시합니다."""
    # 데이터베이스에서 고객 정보 조회
    customer_info = get_customer_by_id(customer_id)
    if customer_info is None:
        tk.messagebox.showerror("오류", "고객 정보를 찾을 수 없습니다.")
        return
    
    print(customer_info)  # 디버깅을 위한 출력

    # 고객 정보 unpacking
    (customer_id, name, birth_year, birth_month, birth_day, age, phone, email, address, gender,
     session_start_date, session_end_date, presenting_problem,
     session_count, special_notes) = customer_info
    
    print(f"birth_month: {birth_month}, Type: {type(birth_month)}")  # 디버깅을 위한 출력
    # Create Toplevel window
    window = tk.Toplevel()
    window.title(f"{name}")
    window.geometry("600x600")

    for i in range(7):
        window.grid_columnconfigure(i, minsize=10)  # 첫 번째 열의 최소 너비를 100픽셀로 설정


    # Create labels and entries for each piece of information
    tk.Label(window, text="이름:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_name_edit = tk.Entry(window, width=3)
    entry_name_edit.grid(row=0, column=1, padx=10, pady=5, sticky="ew", columnspan = 2)
    entry_name_edit.insert(0, name)

    tk.Label(window, text="전화번호:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    phone_str = str(phone)  # Ensure phone is a string
    phone_parts = phone_str.split('-') if phone_str else ['', '', '']
    entry_phone1_edit = tk.Entry(window, width=3)
    entry_phone1_edit.grid(row=1, column=1, padx=0, pady=5)
    entry_phone1_edit.insert(0, phone_parts[0])
    tk.Label(window, text="-", width=1).grid(row=1, column=2, padx=0, pady=5, sticky="ew")
    entry_phone2_edit = tk.Entry(window, width=5)
    entry_phone2_edit.grid(row=1, column=3, padx=0, pady=5)
    entry_phone2_edit.insert(0, phone_parts[1])
    tk.Label(window, text="-", width=1).grid(row=1, column=4, padx=0, pady=5, sticky="ew")
    entry_phone3_edit = tk.Entry(window, width=5)
    entry_phone3_edit.grid(row=1, column=5, padx=0, pady=5)
    entry_phone3_edit.insert(0, phone_parts[2])

    tk.Label(window, text="이메일:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_email_edit = tk.Entry(window, width=3)
    entry_email_edit.grid(row=2, column=1, padx=0, pady=5, sticky="ew", columnspan = 4)
    entry_email_edit.insert(0, email)

    tk.Label(window, text="주소:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_address_edit = tk.Entry(window, width=3)
    entry_address_edit.grid(row=3, column=1, padx=0, pady=5, sticky="ew", columnspan = 4)
    entry_address_edit.insert(0, address)

 


    print(f"Gender from database: {gender}, Type: {type(gender)}")

    gender_var = tk.StringVar(value=gender)  # Initialize StringVar with the gender value from database

    # 성별 버튼 배치
    gender_male_rb = tk.Radiobutton(window, text="남", variable=gender_var, value='남', width=3)
    gender_female_rb = tk.Radiobutton(window, text="여", variable=gender_var, value='여', width=3)
    gender_male_rb.grid(row=0, column=4, padx=10, pady=5, sticky="w")
    gender_female_rb.grid(row=0, column=5, padx=10, pady=5, sticky="w")

    tk.Label(window, text="생년월일:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    entry_birth_year = tk.Entry(window, width=5)
    entry_birth_year.grid(row=5, column=1, padx=0, pady=5)
    entry_birth_year.insert(0, str(birth_year))
    tk.Label(window, text="년", width=1).grid(row=5, column=2, padx=1, pady=5, sticky="w")
    entry_birth_month = tk.Entry(window, width=3)
    entry_birth_month.grid(row=5, column=3, padx=0, pady=5)
    entry_birth_month.insert(0, str(birth_month))
    tk.Label(window, text="월", width=1).grid(row=5, column=4, padx=1, pady=5, sticky="w")
    entry_birth_day = tk.Entry(window, width=3)
    entry_birth_day.grid(row=5, column=5, padx=0, pady=5)
    entry_birth_day.insert(0, str(birth_day))
    tk.Label(window, text="일", width=1).grid(row=5, column=6, padx=1, pady=5, sticky="w")

    tk.Label(window, text="나이:").grid(row=5, column=7, padx=10, pady=5, sticky="w")
    entry_age_edit = tk.Entry(window, width=3)
    entry_age_edit.grid(row=5, column=8, padx=0, pady=5, sticky="ew")
    entry_age_edit.insert(0, age)
    entry_age_edit.config(state='disabled')  # 나이 필드 비활성화


    # 나이 계산 함수
    def update_age(event=None):
        try:
            birth_year = int(entry_birth_year.get().strip())
            birth_month = int(entry_birth_month.get().strip())
            birth_day = int(entry_birth_day.get().strip())

            birth_date = datetime(birth_year, birth_month, birth_day)
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

            entry_age_edit.config(state='normal')
            entry_age_edit.delete(0, tk.END)
            entry_age_edit.insert(0, age)
            entry_age_edit.config(state='disabled')
        except ValueError:
            pass

    entry_birth_year.bind("<KeyRelease>", update_age)
    entry_birth_month.bind("<KeyRelease>", update_age)
    entry_birth_day.bind("<KeyRelease>", update_age)

    

    session_start_part = session_start_date.split('-') if session_start_date else ['', '', '']
    tk.Label(window, text="상담 시작일:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    entry_session_start_year = tk.Entry(window, width=5)
    entry_session_start_year.grid(row=6, column=1, padx=0, pady=5)
    entry_session_start_year.insert(0, str(session_start_part[0]))
    tk.Label(window, text="년", width=1).grid(row=6, column=2, padx=1, pady=5, sticky="w")
    entry_session_start_month = tk.Entry(window, width=3)
    entry_session_start_month.grid(row=6, column=3, padx=0, pady=5)
    entry_session_start_month.insert(0, str(session_start_part[1]))
    tk.Label(window, text="월", width=1).grid(row=6, column=4, padx=1, pady=5, sticky="w")
    entry_session_start_day = tk.Entry(window, width=3)
    entry_session_start_day.grid(row=6, column=5, padx=0, pady=5)
    entry_session_start_day.insert(0, str(session_start_part[2]))
    tk.Label(window, text="일", width=1).grid(row=6, column=6, padx=1, pady=5, sticky="w")

    # 여기에서 session_start_date를 최종적으로 구성
    session_start_date = f"{entry_session_start_year}-{entry_session_start_month}-{entry_session_start_day}" if entry_session_start_year and entry_session_start_month and entry_session_start_day else ''


    session_end_str = str(session_end_date) 
    session_end_part = session_end_str.split('-') if session_end_str else ['', '', '']
    tk.Label(window, text="상담 종료일:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    entry_session_end_year = tk.Entry(window, width=5)
    entry_session_end_year.grid(row=7, column=1, padx=0, pady=5)
    entry_session_end_year.insert(0, str(session_end_part[0]))
    tk.Label(window, text="년", width=1).grid(row=7, column=2, padx=1, pady=5, sticky="w")
    entry_session_end_month = tk.Entry(window, width=3)
    entry_session_end_month.grid(row=7, column=3, padx=0, pady=5)
    entry_session_end_month.insert(0, str(session_end_part[1]))
    tk.Label(window, text="월", width=1).grid(row=7, column=4, padx=1, pady=5, sticky="w")
    entry_session_end_day = tk.Entry(window, width=3)
    entry_session_end_day.grid(row=7, column=5, padx=0, pady=5)
    entry_session_end_day.insert(0, str(session_end_part[2]))
    tk.Label(window, text="일", width=1).grid(row=7, column=6, padx=1, pady=5, sticky="w")
    entry_session_end = f"{entry_session_end_year}-{entry_session_end_month}-{entry_session_end_day}"

    tk.Label(window, text="호소 문제:").grid(row=8, column=0, padx=10, pady=5, sticky="nw")
    entry_presenting_problem = tk.Text(window, height=4, width=5)
    entry_presenting_problem.grid(row=8, column=1, padx=0, pady=5, sticky="ew", columnspan=8)
    entry_presenting_problem.insert("1.0", presenting_problem if presenting_problem else "")
    # Text widget for special notes
    entry_special_notes = tk.Text(entry_presenting_problem, height=4, width=40)
    entry_special_notes.pack(side="left", fill="both", expand=True)
    # Scrollbar for the Text widget
    scrollbar_special_notes = tk.Scrollbar(entry_presenting_problem, command=entry_presenting_problem.yview)
    scrollbar_special_notes.pack(side="right", fill="y")
    # Link scrollbar to Text widget
    entry_special_notes.config(yscrollcommand=scrollbar_special_notes.set)

    tk.Label(window, text="회기수:").grid(row=9, column=0, padx=10, pady=5, sticky="w")
    entry_session_count = tk.Entry(window, width=3)
    entry_session_count.grid(row=9, column=1, padx=0, pady=5, sticky="ew")
    entry_session_count.insert(0, session_count if session_count else "")
    tk.Label(window, text="회").grid(row=9, column=2, padx=0, pady=5, sticky="w")

    tk.Label(window, text="특이사항:").grid(row=10, column=0, padx=10, pady=5, sticky="nw")
    entry_special_notes = tk.Text(window, height=4, width=5)
    entry_special_notes.grid(row=10, column=1, padx=0, pady=5, sticky="ew", columnspan=8)
    entry_special_notes.insert("1.0", special_notes if special_notes else "")
    # Text widget for special notes
    entry_special_notes = tk.Text(entry_special_notes, height=4, width=40)
    entry_special_notes.pack(side="left", fill="both", expand=True)
    # Scrollbar for the Text widget
    scrollbar_special_notes = tk.Scrollbar(entry_special_notes, command=entry_special_notes.yview)
    scrollbar_special_notes.pack(side="right", fill="y")
    # Link scrollbar to Text widget
    entry_special_notes.config(yscrollcommand=scrollbar_special_notes.set)

    # Add save button
    def save_customer():
        name = entry_name_edit.get().strip()
        
        if not name:
            messagebox.showwarning("필수 항목 누락", "이름을 입력해주세요.")
            return
        
        # Optional fields with default empty values
        birth_year = entry_birth_year.get().strip() or ''
        birth_month = entry_birth_month.get().strip() or ''
        birth_day = entry_birth_day.get().strip() or ''
        age = entry_age_edit.get().strip() or '' 
        phone_part1 = entry_phone1_edit.get().strip()
        phone_part2 = entry_phone2_edit.get().strip()
        phone_part3 = entry_phone3_edit.get().strip()
        phone = f"{phone_part1}-{phone_part2}-{phone_part3}" if phone_part1 and phone_part2 and phone_part3 else ''
        email = entry_email_edit.get().strip() or ''
        address = entry_address_edit.get().strip() or ''
        gender = gender_var.get().strip() or ''
        session_start_date = session_start_date.get().strip() or ''
        session_end_date = entry_session_end.get_date().strftime('%Y-%m-%d') if entry_session_end.get_date() else ''
        session_count = entry_session_count.get().strip() or ''
        presenting_problem = entry_presenting_problem.get("1.0", tk.END).strip() or ''
        special_notes = entry_special_notes.get("1.0", tk.END).strip() or ''

        if not validate_birthdate(birth_year, birth_month, birth_day):
            messagebox.showwarning("잘못된 입력", "올바른 생년월일을 입력하십시오.")
            return

        update_customer(customer_id, name, birth_year, birth_month, birth_day, age, phone, email, address, gender,
                            session_start_date, session_end_date, presenting_problem, session_count, special_notes)
            
        messagebox.showinfo("저장 완료", "고객 정보가 저장되었습니다.")
        load_customers(treeview_customers, get_customers, query="")



    save_button = tk.Button(window, text="저장", command=save_customer)
    save_button.grid(row=12, column=0, padx=10, pady=10, sticky="w")

    window.mainloop()




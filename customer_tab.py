# customer_tab.py

import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
from sql import update_customer, delete_customer  # 필요한 경우

def create_customer_tab(notebook, tab_names, customer_id, name, phone, email, address, gender,
                        session_start_date, session_end_date, presenting_problem,
                        session_count, special_notes, birth_year, birth_month, birth_day, age):
    tab_name = name

    # Check if the tab already exists
    if tab_name in tab_names:
        notebook.select(tab_names[tab_name])
        return

    new_tab = ttk.Frame(notebook)

    # Add the tab to the notebook
    notebook.add(new_tab, text=f"{tab_name} [x]", sticky="nsew")

    # Add X button to the tab frame
    close_button = tk.Button(new_tab, text="X", command=lambda: close_tab(tab_name, new_tab))
    close_button.grid(row=0, column=1, padx=5, pady=5, sticky='ne')

    # Create labels and entries for each piece of information
    tk.Label(new_tab, text="이름:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(new_tab, text="전화번호:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    tk.Label(new_tab, text="이메일:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    tk.Label(new_tab, text="주소:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    tk.Label(new_tab, text="성별:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    tk.Label(new_tab, text="생년월일:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    tk.Label(new_tab, text="나이:").grid(row=6, column=4, padx=10, pady=5, sticky="w")  # 나이 라벨 추가
    tk.Label(new_tab, text="상담 시작일:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    tk.Label(new_tab, text="상담 종료일:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
    tk.Label(new_tab, text="호소 문제:").grid(row=9, column=0, padx=10, pady=5, sticky="nw")
    tk.Label(new_tab, text="회기수:").grid(row=10, column=0, padx=10, pady=5, sticky="w")
    tk.Label(new_tab, text="특이사항:").grid(row=11, column=0, padx=10, pady=5, sticky="nw")

    phone_parts = phone.split('-') if phone else ['', '', '']

    # Display and edit phone number
    entry_phone1_edit = tk.Entry(new_tab, width=5)
    entry_phone1_edit.grid(row=2, column=1, padx=10, pady=5)
    entry_phone1_edit.insert(0, phone_parts[0])

    tk.Label(new_tab, text="-").grid(row=2, column=2, padx=0, pady=5)

    entry_phone2_edit = tk.Entry(new_tab, width=5)
    entry_phone2_edit.grid(row=2, column=3, padx=0, pady=5)
    entry_phone2_edit.insert(0, phone_parts[1])

    tk.Label(new_tab, text="-").grid(row=2, column=4, padx=0, pady=5)

    entry_phone3_edit = tk.Entry(new_tab, width=5)
    entry_phone3_edit.grid(row=2, column=5, padx=0, pady=5)
    entry_phone3_edit.insert(0, phone_parts[2])

    # Display and edit other fields
    entry_name_edit = tk.Entry(new_tab)
    entry_name_edit.grid(row=1, column=1)
    entry_name_edit.insert(0, name)

    entry_email_edit = tk.Entry(new_tab)
    entry_email_edit.grid(row=3, column=1)
    entry_email_edit.insert(0, email)

    entry_address_edit = tk.Entry(new_tab)
    entry_address_edit.grid(row=4, column=1)
    entry_address_edit.insert(0, address)

    # Gender (radio buttons)
    gender_var = tk.StringVar(value=gender)
    gender_male_rb = tk.Radiobutton(new_tab, text="남", variable=gender_var, value='남')
    gender_male_rb.grid(row=5, column=1, padx=10, pady=5, sticky="w")
    gender_female_rb = tk.Radiobutton(new_tab, text="여", variable=gender_var, value='여')
    gender_female_rb.grid(row=5, column=2, padx=10, pady=5, sticky="w")

    # Birthdate and age
    entry_birth_year = tk.Entry(new_tab, width=5)
    entry_birth_year.grid(row=6, column=1, padx=10, pady=5)
    entry_birth_year.insert(0, birth_year)

    entry_birth_month = tk.Entry(new_tab, width=5)
    entry_birth_month.grid(row=6, column=2, padx=10, pady=5)
    entry_birth_month.insert(0, birth_month)

    entry_birth_day = tk.Entry(new_tab, width=5)
    entry_birth_day.grid(row=6, column=3, padx=10, pady=5)
    entry_birth_day.insert(0, birth_day)

    entry_age_edit = tk.Entry(new_tab)
    entry_age_edit.grid(row=6, column=5, padx=10, pady=5)
    entry_age_edit.insert(0, age)

    # Dates
    entry_session_start = DateEntry(new_tab, date_pattern='yyyy-mm-dd')
    entry_session_start.grid(row=7, column=1, padx=10, pady=5, sticky="ew")
    entry_session_start.set_date(datetime.strptime(session_start_date, '%Y-%m-%d') if session_start_date else datetime.today())

    entry_session_end = DateEntry(new_tab, date_pattern='yyyy-mm-dd')
    entry_session_end.grid(row=8, column=1, padx=10, pady=5, sticky="ew")
    entry_session_end.set_date(datetime.strptime(session_end_date, '%Y-%m-%d') if session_end_date else datetime.today())

    # Presenting problem and special notes
    entry_presenting_problem = tk.Text(new_tab, height=4, width=40)
    entry_presenting_problem.grid(row=9, column=1, padx=10, pady=5, sticky="ew", columnspan=4)
    entry_presenting_problem.insert("1.0", presenting_problem if presenting_problem else "")

    entry_session_count = tk.Entry(new_tab)
    entry_session_count.grid(row=10, column=1, padx=10, pady=5, sticky="ew")
    entry_session_count.insert(0, session_count if session_count else "")

    entry_special_notes = tk.Text(new_tab, height=4, width=40)
    entry_special_notes.grid(row=11, column=1, padx=10, pady=5, sticky="ew", columnspan=4)
    entry_special_notes.insert("1.0", special_notes if special_notes else "")

    def save_edits():
        updated_name = entry_name_edit.get().strip()
        updated_phone = f"{entry_phone1_edit.get()}-{entry_phone2_edit.get()}-{entry_phone3_edit.get()}"
        updated_email = entry_email_edit.get().strip()
        updated_address = entry_address_edit.get().strip()
        updated_gender = gender_var.get().strip()
        updated_session_start = entry_session_start.get_date().strftime('%Y-%m-%d')
        updated_session_end = entry_session_end.get_date().strftime('%Y-%m-%d')
        updated_presenting_problem = entry_presenting_problem.get("1.0", tk.END).strip()
        updated_session_count = entry_session_count.get().strip()
        updated_special_notes = entry_special_notes.get("1.0", tk.END).strip()

        # 생년월일을 연도, 월, 일로 조합
        updated_birth_year = entry_birth_year.get().strip()
        updated_birth_month = entry_birth_month.get().strip()
        updated_birth_day = entry_birth_day.get().strip()
        updated_birthdate = f"{updated_birth_year}-{int(updated_birth_month):02d}-{int(updated_birth_day):02d}"
        updated_age = entry_age_edit.get().strip()

        # Update customer information using ID
        update_customer(customer_id, updated_name, updated_phone, updated_email, updated_address,
                        updated_gender, updated_session_start, updated_session_end,
                        updated_presenting_problem, updated_session_count, updated_special_notes,
                        updated_birthdate, updated_age)
        messagebox.showinfo("저장 완료", "저장되었습니다!")

    tk.Button(new_tab, text="저장", command=save_edits).grid(row=12, column=1, padx=10, pady=10, sticky="w")



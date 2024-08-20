import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
from sql import update_customer, delete_customer, validate_birthdate, load_customers, get_customers, get_customer_by_id

def create_customer_window(customer_id, treeview_customers):
    """고객 ID로 새 창을 열고 정보를 표시합니다."""
    # 데이터베이스에서 고객 정보 조회
    customer_info = get_customer_by_id(customer_id)
    if customer_info is None:
        tk.messagebox.showerror("오류", "고객 정보를 찾을 수 없습니다.")
        return

    # 고객 정보 unpacking
    (customer_id, name, phone, email, address, gender,
     session_start_date, session_end_date, presenting_problem,
     session_count, special_notes, birth_year, birth_month, birth_day, age) = customer_info

    # Create Toplevel window
    window = tk.Toplevel()
    window.title(f"Customer Details - {name}")
    window.geometry("600x600")

    # Create labels and entries for each piece of information
    tk.Label(window, text="이름:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(window, text="전화번호:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    tk.Label(window, text="이메일:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    tk.Label(window, text="주소:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    tk.Label(window, text="성별:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    tk.Label(window, text="생년월일:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    tk.Label(window, text="나이:").grid(row=6, column=4, padx=10, pady=5, sticky="w")  # 나이 라벨 추가
    tk.Label(window, text="상담 시작일:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    tk.Label(window, text="상담 종료일:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
    tk.Label(window, text="호소 문제:").grid(row=9, column=0, padx=10, pady=5, sticky="nw")
    tk.Label(window, text="회기수:").grid(row=10, column=0, padx=10, pady=5, sticky="w")
    tk.Label(window, text="특이사항:").grid(row=11, column=0, padx=10, pady=5, sticky="nw")

    phone_parts = phone.split('-') if phone else ['', '', '']

    # Display and edit phone number
    entry_phone1_edit = tk.Entry(window, width=5)
    entry_phone1_edit.grid(row=2, column=1, padx=10, pady=5)
    entry_phone1_edit.insert(0, phone_parts[0])

    tk.Label(window, text="-").grid(row=2, column=2, padx=0, pady=5)

    entry_phone2_edit = tk.Entry(window, width=5)
    entry_phone2_edit.grid(row=2, column=3, padx=0, pady=5)
    entry_phone2_edit.insert(0, phone_parts[1])

    tk.Label(window, text="-").grid(row=2, column=4, padx=0, pady=5)

    entry_phone3_edit = tk.Entry(window, width=5)
    entry_phone3_edit.grid(row=2, column=5, padx=0, pady=5)
    entry_phone3_edit.insert(0, phone_parts[2])

    # Display and edit other fields
    entry_name_edit = tk.Entry(window)
    entry_name_edit.grid(row=1, column=1)
    entry_name_edit.insert(0, name)

    entry_email_edit = tk.Entry(window)
    entry_email_edit.grid(row=3, column=1)
    entry_email_edit.insert(0, email)

    entry_address_edit = tk.Entry(window)
    entry_address_edit.grid(row=4, column=1)
    entry_address_edit.insert(0, address)

    # Gender (radio buttons)
    gender_var = tk.StringVar(value=gender)
    gender_male_rb = tk.Radiobutton(window, text="남", variable=gender_var, value='남')
    gender_male_rb.grid(row=5, column=1, padx=10, pady=5, sticky="w")
    gender_female_rb = tk.Radiobutton(window, text="여", variable=gender_var, value='여')
    gender_female_rb.grid(row=5, column=2, padx=10, pady=5, sticky="w")

    # Birthdate and age
    entry_birth_year = tk.Entry(window, width=5)
    entry_birth_year.grid(row=6, column=1, padx=10, pady=5)
    entry_birth_year.insert(0, birth_year)

    entry_birth_month = tk.Entry(window, width=5)
    entry_birth_month.grid(row=6, column=2, padx=10, pady=5)
    entry_birth_month.insert(0, birth_month)

    entry_birth_day = tk.Entry(window, width=5)
    entry_birth_day.grid(row=6, column=3, padx=10, pady=5)
    entry_birth_day.insert(0, birth_day)

    entry_age_edit = tk.Entry(window)
    entry_age_edit.grid(row=6, column=5, padx=10, pady=5)
    entry_age_edit.insert(0, age)
    entry_age_edit.config(state='disabled')  # 나이 필드 비활성화

    # 나이 계산 함수
    def update_age(event=None):
        try:
            # 사용자가 입력한 생년월일을 가져옴
            birth_year = int(entry_birth_year.get().strip())
            birth_month = int(entry_birth_month.get().strip())
            birth_day = int(entry_birth_day.get().strip())

            # 현재 날짜와 비교하여 나이 계산
            birth_date = datetime(birth_year, birth_month, birth_day)
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

            # 계산된 나이 업데이트
            entry_age_edit.config(state='normal')
            entry_age_edit.delete(0, tk.END)
            entry_age_edit.insert(0, age)
            entry_age_edit.config(state='disabled')
        except ValueError:
            # 생년월일이 완전하지 않을 경우 예외 처리
            pass

    # 생년월일 입력 시 나이 업데이트를 위한 이벤트 바인딩
    entry_birth_year.bind("<KeyRelease>", update_age)
    entry_birth_month.bind("<KeyRelease>", update_age)
    entry_birth_day.bind("<KeyRelease>", update_age)

    # Dates
    entry_session_start = DateEntry(window, date_pattern='yyyy-mm-dd')
    entry_session_start.grid(row=7, column=1, padx=10, pady=5, sticky="ew")
    entry_session_start.set_date(datetime.strptime(session_start_date, '%Y-%m-%d') if session_start_date else datetime.today())

    entry_session_end = DateEntry(window, date_pattern='yyyy-mm-dd')
    entry_session_end.grid(row=8, column=1, padx=10, pady=5, sticky="ew")
    entry_session_end.set_date(datetime.strptime(session_end_date, '%Y-%m-%d') if session_end_date else datetime.today())

    # Presenting problem and special notes
    entry_presenting_problem = tk.Text(window, height=2, width=40)
    entry_presenting_problem.grid(row=9, column=1, padx=10, pady=5, sticky="ew", columnspan=4)
    entry_presenting_problem.insert("1.0", presenting_problem if presenting_problem else "")

    entry_session_count = tk.Entry(window)
    entry_session_count.grid(row=10, column=1, padx=10, pady=5, sticky="ew")
    entry_session_count.insert(0, session_count if session_count else "")

    entry_special_notes = tk.Text(window, height=4, width=40)
    entry_special_notes.grid(row=11, column=1, padx=10, pady=5, sticky="ew", columnspan=4)
    entry_special_notes.insert("1.0", special_notes if special_notes else "")

    # Add save button
    def save_changes():
        # 수정을 데이터베이스에 저장하는 코드 추가
        pass

    save_button = tk.Button(window, text="저장", command=save_changes)
    save_button.grid(row=12, column=0, padx=10, pady=10, sticky="w")

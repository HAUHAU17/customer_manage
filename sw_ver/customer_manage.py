import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font
from tkcalendar import DateEntry
import sql  # sql.py 파일을 import
from datetime import datetime
import pandas as pd
import json

# GUI 애플리케이션 생성
root = tk.Tk()
root.title("고객 관리 프로그램")
root.geometry("1400x800")  # 메인 창 초기 크기 설정

# 기본 폰트 크기
BASE_FONT_SIZE = 10
custom_font = ("Arial", BASE_FONT_SIZE)
settings = {}

# Treeview 설정
headers = [
    "ID", "이름", "생년월일", "년", "월", "일", "나이", "메일", "성별", "남자", "여자", "전화번호", "주소", "상담시작일", "시작연도", "시작월", "시작일", "상담종료일", "종료연도", "종료월", "종료일", "호소문제", "회기 수", "특이사항"
]
viewonly_headers = [
    "ID", "이름", "생년월일", "나이", "메일", "성별", "전화번호", "주소", "상담시작일", "상담종료일", "회기 수"
]
export_headers = [
    "ID", "이름", "생년월일", "나이", "메일", "성별", "전화번호", "주소", "상담시작일", "상담종료일", "호소문제", "회기 수", "특이사항"
]
treeview_users = ttk.Treeview(root, columns=viewonly_headers, show='headings')

# 기본 열 너비 설정
column_widths = {
    "ID": 10,
    "이름": 50,
    "생년월일": 100,
    "나이": 10,
    "메일": 150,
    "성별": 10,
    "전화번호": 100,
    "주소": 300,
    "상담시작일": 100,
    "상담종료일": 100,
    "회기 수": 10
}

for header in viewonly_headers:
    treeview_users.heading(header, text=header)
    treeview_users.column(header, width=column_widths.get(header, 100), anchor=tk.CENTER)

treeview_users.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

gender_var = tk.StringVar()

def update_font_size(percent, all_widgets):
    size = int(BASE_FONT_SIZE * percent / 100)
    global custom_font, settings
    custom_font = ("Arial", size)

    # 적용할 위젯 리스트
    for widget in all_widgets:
        widget.config(font=custom_font)
    
    # Treeview의 스타일 업데이트
    style = ttk.Style()
    style.configure("Treeview", font=custom_font)

    settings["font_size"] = percent
    save_settings(settings)

def set_font_size(percent, all_widgets, var):
    update_font_size(percent, all_widgets)
    var.set(percent)  # 현재 선택된 폰트 크기를 업데이트
    update_checkmarks()  # 체크 표시 업데이트

def update_checkmarks():
    global font_menu
    for index, percent in enumerate(percent_buttons):
        if percent == var.get():
            font_menu.entryconfig(index, indicatoron=True, selectcolor="lightgray", background="lightgray", foreground="blue")
        else:
            font_menu.entryconfig(index, indicatoron=False, background="white", foreground="black")

def create_menu(root, all_widgets):
    global font_menu, percent_buttons, var
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    
    settings_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="추가기능", menu=settings_menu)
    
    font_menu = tk.Menu(settings_menu, tearoff=0)
    settings_menu.add_cascade(label="글꼴", menu=font_menu)

    # 퍼센트 항목 추가
    percent_buttons = [100, 110, 120, 130, 140, 150]

    # 현재 선택된 폰트 크기를 저장할 변수
    var = tk.IntVar(value=settings.get("font_size", 100))
    
    for percent in percent_buttons:
        font_menu.add_radiobutton(label=f"{percent}%", variable=var, value=percent, command=lambda p=percent: set_font_size(p, all_widgets, var))
    
    # 초기 체크 표시 업데이트
    update_checkmarks()

def update_age(year, month, day):
    today = datetime.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age

def validate_integer(input_value):
    """정수만 허용하는 검증 함수"""
    return input_value.isdigit() or input_value == ""

def validate_phone(input_value):
    """전화번호에 숫자와 공백만 허용하는 검증 함수"""
    return all(char.isdigit() or char.isspace() for char in input_value) or input_value == ""

def validate_hyphen(input_value):
    """"-"만 허용하는 검증 함수"""
    return  input_value!="-"

# 세션 저장 함수
def save_session_data(session_window, session_data):
    # 여기에 데이터베이스 저장 로직을 추가하세요.
    # 예: cursor.execute("INSERT INTO sessions (field1, field2, ...) VALUES (?, ?, ...)", (value1, value2, ...))
    print("세션 데이터 저장:", session_data)  # 이 부분은 실제로 DB에 저장하는 코드로 대체해야 합니다.
    messagebox.showinfo("저장 완료", "세션 정보가 저장되었습니다.")
    session_window.destroy()

# 입력 행 추가 함수
def add_entry_row(session_window, labels, session_data, row_num, add_button, save_button):
    entries = []
    
    # '회차' 라벨 추가
    tk.Label(session_window, text=f"{row_num}회기").grid(row=row_num, column=0, padx=10, pady=5)

    for i, label_text in enumerate(labels[1:], start=1):
        entry = tk.Entry(session_window)
        entry.grid(row=row_num, column=i, padx=10, pady=5)
        entries.append(entry)
    
    # 각 행의 입력 필드를 session_data 리스트에 추가
    session_data[row_num] = entries

    # 첫 번째 행이 아닌 경우에만 삭제 버튼 추가
    if row_num != 1:
        delete_button = tk.Button(session_window, text="삭제", command=lambda: delete_entry_row(session_window, labels, session_data, row_num, add_button, save_button))
        delete_button.grid(row=row_num, column=len(labels), padx=10, pady=5)

    # '추가', '저장' 버튼 위치 재조정
    add_button.grid(row=row_num + 1, column=len(labels), padx=10, pady=5)
    save_button.grid(row=row_num + 1, column=len(labels) + 1, columnspan=2, pady=10)

# 입력 행 삭제 함수
def delete_entry_row(session_window, labels, session_data, row_num, add_button, save_button):
    # 해당 행의 모든 위젯 숨기기
    for widget in session_window.grid_slaves(row=row_num):
        widget.grid_forget()
    
    # 해당 행의 데이터 삭제
    print("length : ", len(session_data), ", row : ", row_num)
    del session_data[row_num]
    print("length : ", len(session_data))

    # 행 번호 재조정
    for r in range(row_num, len(session_data) + 1):
        for widget in session_window.grid_slaves(row=r+1):
            widget.grid(row=r)
            
    # 데이터 재조정
    session_data_adjusted = {}
    for i, (k, v) in enumerate(session_data.items()):
        session_data_adjusted[i+1] = v
    
    session_data.clear()
    session_data.update(session_data_adjusted)
    
    # 모든 '회차' 라벨 업데이트
    for r, widgets in session_data.items():
        label = session_window.grid_slaves(row=r, column=0)[0]
        label.config(text=f"{r}회기")
        new_row_num = r
    
    print("new_row_num :", new_row_num)
    # 삭제 버튼의 command 재설정
    if new_row_num != 1:
        delete_button = tk.Button(session_window, text="삭제", command=lambda r=new_row_num: delete_entry_row(session_window, labels, session_data, r, add_button, save_button))
        delete_button.grid(row=new_row_num, column=len(labels), padx=10, pady=5)
    
    # '추가' 버튼 위치를 재조정된 마지막 행의 우측으로 이동
    add_button.grid(row=len(session_data) + 2, column=len(labels), padx=10, pady=5)
    # 저장 버튼 생성
    save_button.grid(row=len(session_data) + 2, column=len(labels) + 1, columnspan=2, pady=10)

# 회기 세부 정보 입력 창을 여는 함수
def open_sessions(window):
    session_window = tk.Toplevel(window)
    session_window.title("회기 세부 정보")
    session_window.geometry("900x600")  # 새 창 크기 설정
    
    # 세션 데이터 저장할 딕셔너리
    session_data = {}

    # 테이블 헤더 생성
    labels = ["회기", "날짜", "상담내용"]
    for i, label_text in enumerate(labels):
        label = tk.Label(session_window, text=label_text)
        label.grid(row=0, column=i, padx=10, pady=5)

    # 첫 번째 입력 행 추가
    add_button = tk.Button(session_window, text="추가", command=lambda: add_entry_row(session_window, labels, session_data, len(session_data) + 1, add_button, save_button))
    save_button = tk.Button(session_window, text="저장", command=lambda: save_session_data(session_window, {k: [e.get() for e in v] for k, v in session_data.items()}))

    # 초기 설정
    add_entry_row(session_window, labels, session_data, 1, add_button, save_button)

def create_field_entries(window):
    """필드 및 라벨 설정을 함수화하여 중복 제거."""
    labels_and_fields = {}
    special_entries = {}
    window_widgets = []
    
    def calculate_age():
        try:
            """생년월일을 입력받아 나이를 계산합니다."""
            year_entry = labels_and_fields.get("년")
            month_entry = labels_and_fields.get("월")
            day_entry = labels_and_fields.get("일")

            birth_year = int(year_entry.get())
            birth_month = int(month_entry.get())
            birth_day = int(day_entry.get())
            birth_date = datetime(birth_year, birth_month, birth_day)

            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            
            age_entry = labels_and_fields.get("나이")
            if age_entry:
                age_entry.config(state=tk.NORMAL)  # Enable editing
                age_entry.delete(0, tk.END)
                age_entry.insert(0, "-" if age == 0 else str(age))
                age_entry.config(state=tk.DISABLED)  # Disable editing
        except ValueError:
            pass  # 값이 입력되기 전에 발생하는 오류를 무시
    
    # Helper function to update date entry widget
    def on_key_release(event):
        # 모든 필드가 채워지면 나이 계산
        if all(labels_and_fields.get(field).get() for field in ["년", "월", "일"]):
            calculate_age()
    
    for header in headers:
        if header in ["ID"]:
            continue
        elif header in ["회기 수"]:
            entry = tk.Entry(window, width=10, validate="key", validatecommand=(window.register(validate_integer), "%P"))
            session_button = tk.Button(window, text="상세", command=lambda: open_sessions(window))
            special_entries[header] = session_button
        elif header in ["상담시작일", "시작연도", "상담종료일", "종료연도"]:
            entry = tk.Entry(window, width=10, validate="key", validatecommand=(window.register(validate_integer), "%P"))
        elif header in ["시작월", "시작일", "종료월", "종료일"]:
            entry = tk.Entry(window, width=5, validate="key", validatecommand=(window.register(validate_integer), "%P"))
        elif header in ["전화번호"]:
            entry = tk.Entry(window, width=20, validate="key", validatecommand=(window.register(validate_phone), "%P"))
        elif header in ["생년월일", "년", "월", "일", "나이"]:
            # Create lists for year, month, and day dropdowns
            if header in ["년"]:
                entry = tk.Entry(window, width=10, validate="key", validatecommand=(window.register(validate_integer), "%P"))
                entry.bind('<KeyRelease>', on_key_release)
            elif header in ["월"]:
                entry = tk.Entry(window, width=5, validate="key", validatecommand=(window.register(validate_integer), "%P"))
                entry.bind('<KeyRelease>', on_key_release)
            elif header in ["일"]:
                entry = tk.Entry(window, width=5, validate="key", validatecommand=(window.register(validate_integer), "%P"))
                entry.bind('<KeyRelease>', on_key_release)
            elif header in ["생년월일"]:
                # Entry widget for date
                entry = tk.Entry(window, width=5)
            else:
                entry = tk.Entry(window, width=5, validate="key", validatecommand=(window.register(validate_integer), "%P"))
                entry.config(state=tk.DISABLED)  # Disable editing
        elif header in ["특이사항"]:
            entry = tk.Text(window, height=10, width=60)
        elif header in ["호소문제"]:
            entry = tk.Text(window, height=3, width=60)
        elif header in ["메일"]:
            entry = tk.Entry(window, width=30, validate="key", validatecommand=(window.register(validate_hyphen), "%P"))
        elif header in ["주소"]:
            entry = tk.Entry(window, width=60, validate="key", validatecommand=(window.register(validate_hyphen), "%P"))
        elif header in ["성별", "남자", "여자"]:
            if header in ["남자"]:
                entry = tk.Radiobutton(window, text="남", variable=gender_var, value="남")
            elif header in ["여자"]:
                entry = tk.Radiobutton(window, text="여", variable=gender_var, value="여")
            else:
                entry = tk.Entry(window, width=10)
            gender_var.set("-")
        else:
            entry = tk.Entry(window, width=10, validate="key", validatecommand=(window.register(validate_hyphen), "%P"))
        
        labels_and_fields[header] = entry
        window_widgets.append(entry)
    
    # 메뉴바 생성
    update_font_size(settings["font_size"], window_widgets)
    create_menu(window, window_widgets)  # Pass the widget list to create_menu
    
    return labels_and_fields, special_entries

def grid_field_entries(labels_and_fields, special_entries, window):
    """필드 및 라벨의 그리드를 설정."""
    row = 0
    for label_text, entry in labels_and_fields.items():
        if label_text == "특이사항" or label_text == "호소문제":
            tk.Label(window, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky='ew')
            scrollbar = tk.Scrollbar(window, command=entry.yview)
            entry.config(yscrollcommand=scrollbar.set)

            # 특이사항 필드의 프레임과 텍스트 및 스크롤 바를 배치
            column_length = 20
            entry.grid(row=row, column=1, columnspan=column_length, padx=1, pady=5, sticky="w")
            scrollbar.grid(row=row, column=column_length+1, pady=5, sticky="ns")
            row += 1
        elif label_text == "생년월일" or label_text == "성별" or label_text == "상담시작일" or label_text == "상담종료일":
            # Handling the special case for "생년월일", "성별", "상담시작일", "상담종료일"
            tk.Label(window, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky='ew')
        elif label_text == "년":
            entry.grid(row=row, column=1, padx=1, pady=5, sticky='w')
            tk.Label(window, text=label_text).grid(row=row, column=2, padx=1, pady=5, sticky='w')
        elif label_text == "월":
            entry.grid(row=row, column=3, padx=1, pady=5, sticky='e')
            tk.Label(window, text=label_text).grid(row=row, column=4, padx=1, pady=5, sticky='w')
        elif label_text == "일":
            entry.grid(row=row, column=5, padx=1, pady=5, sticky='e')
            tk.Label(window, text=label_text).grid(row=row, column=6, padx=1, pady=5, sticky='w')
            row += 1
        elif label_text == "남자":
            entry.grid(row=row, column=1, padx=1, pady=5, sticky='w')
        elif label_text == "여자":
            entry.grid(row=row, column=2, padx=1, pady=5, sticky='w')
            row += 1
        elif label_text == "시작연도":
            entry.grid(row=row, column=1, padx=1, pady=5, sticky='w')
            tk.Label(window, text="년").grid(row=row, column=2, padx=1, pady=5, sticky='w')
        elif label_text == "시작월":
            entry.grid(row=row, column=3, padx=1, pady=5, sticky='e')
            tk.Label(window, text="월").grid(row=row, column=4, padx=1, pady=5, sticky='w')
        elif label_text == "시작일":
            entry.grid(row=row, column=5, padx=1, pady=5, sticky='e')
            tk.Label(window, text="일").grid(row=row, column=6, padx=1, pady=5, sticky='w')
            row += 1
        elif label_text == "종료연도":
            entry.grid(row=row, column=1, padx=1, pady=5, sticky='w')
            tk.Label(window, text="년").grid(row=row, column=2, padx=1, pady=5, sticky='w')
        elif label_text == "종료월":
            entry.grid(row=row, column=3, padx=1, pady=5, sticky='e')
            tk.Label(window, text="월").grid(row=row, column=4, padx=1, pady=5, sticky='w')
        elif label_text == "종료일":
            entry.grid(row=row, column=5, padx=1, pady=5, sticky='e')
            tk.Label(window, text="일").grid(row=row, column=6, padx=1, pady=5, sticky='w')
            row += 1
        else:
            tk.Label(window, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky='ew')
            if label_text == "이름" or label_text == "나이":
                entry.grid(row=row, column=1, padx=1, pady=5, sticky='w')
                row += 1
            elif label_text == "회기 수":
                session_button = special_entries[label_text]
                entry.grid(row=row, column=1, padx=1, pady=5, sticky='w')
                session_button.grid(row=row, column=2, padx=1, pady=5, sticky='w')
                row += 1
            else:
                entry.grid(row=row, column=1, columnspan=20, padx=1, pady=5, sticky='w')
                row += 1

def populate_fields(entries, user_data):
    """기존 데이터를 필드에 채워 넣음."""
    # 딕셔너리 항목을 리스트로 변환
    items = list(entries.items())
    
    for label, entry in items[0:]:
        index = headers.index(label) + 0  # ID가 첫 번째 필드이므로 +1
            # tk.Text, tk.Entry를, tk.Radiobutton 구분하여 처리
        if isinstance(entry, tk.Text):
            entry.delete("1.0", tk.END)  # 기존 내용을 삭제
            entry.insert("1.0", user_data[index])  # 텍스트 삽입
        elif isinstance(entry, tk.Radiobutton):
            if user_data[index] == "o":
                if label in ["남자"]:
                    gender_var.set("남")  # 남성 선택
                elif label in ["여자"]:
                    gender_var.set("여")  # 여성 선택
        elif isinstance(entry, tk.Button):
            pass
        else:
            if label in ["나이"]:
                entry.config(state=tk.NORMAL)  # Enable editing
                entry.delete(0, tk.END)  # 기존 내용을 삭제
                entry.insert(0, user_data[index])  # 텍스트 삽입
                entry.config(state=tk.DISABLED) # Disable editing
            else:
                entry.delete(0, tk.END)  # 기존 내용을 삭제
                entry.insert(0, user_data[index])  # 텍스트 삽입

def save_user_data(values, user_id=None):
    """사용자 데이터를 저장 또는 업데이트."""
    try:
        # 상담시작/종료일 병합
        start_year = values.get("시작연도", "").strip()
        start_month = values.get("시작월", "").strip()
        start_day = values.get("시작일", "").strip()
        end_year = values.get("종료연도", "").strip()
        end_month = values.get("종료월", "").strip()
        end_day = values.get("종료일", "").strip()
        
        # 상담시작일 기본값 설정
        if not start_year or not start_month or not start_day:
            consultation_start = "-"
        else:
            try:
                start_year = int(start_year)
                start_month = int(start_month)
                start_day = int(start_day)
                consultation_start = f"{start_year}-{start_month:02d}-{start_day:02d}"
            except ValueError:
                consultation_start = "-"  # 변환 실패 시 기본값 설정
        
        # 상담종료일 기본값 설정
        if not end_year or not end_month or not end_day:
            consultation_end = "-"
        else:
            try:
                end_year = int(end_year)
                end_month = int(end_month)
                end_day = int(end_day)
                consultation_end = f"{end_year}-{end_month:02d}-{end_day:02d}"
            except ValueError:
                consultation_end = "-"  # 변환 실패 시 기본값 설정
        
        # 생년월일 병합
        year = values.get("년", "").strip()
        month = values.get("월", "").strip()
        day = values.get("일", "").strip()
        
        # 기본값 설정
        if not year or not month or not day:
            birth = "-"
            age = "-"
        else:
            # 숫자로 변환하고 예외 처리
            age = values.get("나이", 0)
            try:
                year = int(year)
                month = int(month)
                day = int(day)
                birth = f"{year}-{month:02d}-{day:02d}"
            except ValueError:
                birth = "-"  # 변환 실패 시 기본값 설정
        
        #성별
        gender = gender_var.get()
        male = "o" if gender == "남" else ""
        female = "o" if gender == "여" else ""

        # 문자열이 숫자일 경우에만 정수로 변환
        value_sessions = values.get("회기 수", 0)
        
        # 나이, 회기 수 정수값여부 체크
        if value_sessions.isdigit():
            sessions = int(value_sessions)
        else:
            sessions = "-"  # 기본값
        
        if values["이름"]:
            if user_id:
                sql.update_user(
                    user_id,
                    name=values.get("이름", "") or "-",
                    birth=birth,
                    year=year,
                    month=month,
                    day=day,
                    age=age,
                    email=values.get("메일", "") or "-",
                    gender=gender_var.get() or "-",
                    male=male,
                    female=female,
                    phone=values.get("전화번호", "") or "-",
                    address=values.get("주소", "") or "-",
                    consultation_start=consultation_start,
                    start_year = start_year,
                    start_month = start_month,
                    start_day = start_day,
                    consultation_end=consultation_end,
                    end_year = end_year,
                    end_month = end_month,
                    end_day = end_day,
                    issue=values.get("호소문제", ""),
                    sessions=sessions,
                    notes=values.get("특이사항", "")
                )
                messagebox.showinfo("편집 완료", "리스트가 수정되었습니다.")
            else:
                sql.create_user(
                    name=values.get("이름", "") or "-",
                    birth=birth,
                    year=year,
                    month=month,
                    day=day,
                    age=age,
                    email=values.get("메일", "") or "-",
                    gender=gender_var.get() or "-",
                    male=male,
                    female=female,
                    phone=values.get("전화번호", "") or "-",
                    address=values.get("주소", "") or "-",
                    consultation_start=consultation_start,
                    start_year = start_year,
                    start_month = start_month,
                    start_day = start_day,
                    consultation_end=consultation_end,
                    end_year = end_year,
                    end_month = end_month,
                    end_day = end_day,
                    issue=values.get("호소문제", ""),
                    sessions=sessions,
                    notes=values.get("특이사항", "")
                )
                messagebox.showinfo("생성 완료", "생성되었습니다.")
            read_users_gui()
        else:
            messagebox.showwarning("Input Error", "올바른 항목을 입력하세요.")
    except Exception as e:
        messagebox.showerror("Error", f"오류가 발생했습니다: {e}")

def open_create_user_window():
    create_window = tk.Toplevel(root)
    create_window.title("신규 생성")
    create_window.geometry("800x600")  # 새 창 크기 설정

    entries, special_entries = create_field_entries(create_window)
    grid_field_entries(entries, special_entries, create_window)

    def save_new_user():
        values = {
            label: (entry.get() if isinstance(entry, tk.Entry) else 
            entry.get("1.0", tk.END).strip() if isinstance(entry, tk.Text) else 
            entry.get_date() if isinstance(entry, DateEntry) else None)
            for label, entry in entries.items()
        }
        save_user_data(values)
        create_window.destroy()
    
    button_save = tk.Button(create_window, text="저장", command=save_new_user)
    button_save.grid(row=len(headers), column=20, padx=5, pady=5)

def open_update_window(user_id):
    user_data = [row for row in sql.read_users() if str(row[0]) == user_id][0]
    update_window = tk.Toplevel(root)
    update_window.title("편집")
    update_window.geometry("800x600")  # 새 창 크기 설정

    entries, special_entries = create_field_entries(update_window)
    grid_field_entries(entries, special_entries, update_window)

    # 기존 데이터로 필드 채우기
    populate_fields(entries, user_data)

	# 새 창 열릴 때 Name 입력 필드에 포커스
    entry_name = entries["이름"]
    entry_name.focus_set()
    
    def save_updates():
        values = {
            label: (entry.get() if isinstance(entry, tk.Entry) else 
            entry.get("1.0", tk.END).strip() if isinstance(entry, tk.Text) else 
            entry.get_date() if isinstance(entry, DateEntry) else None)
            for label, entry in entries.items()
        }
        save_user_data(values, user_id=user_id)
        update_window.destroy()
    
    button_export = tk.Button(update_window, text="상세 출력", command=lambda: export_to_excel(user_id=user_id))
    button_export.grid(row=0, column=20, padx=5, pady=5)

    button_save = tk.Button(update_window, text="저장", command=save_updates)
    button_save.grid(row=len(headers), column=20, padx=5, pady=5)

def read_users_gui(search_query=None):
    treeview_users.delete(*treeview_users.get_children())
    rows = sql.read_users(search_query)  # 검색 쿼리를 전달
    
    for row in rows:
        formatted_row = list(row)
        if not formatted_row[3] or not formatted_row[3] or not formatted_row[3]:
            age = "-"
        else:
            age = update_age(formatted_row[3], formatted_row[4], formatted_row[5])
        sql.update_user(
                            formatted_row[0],
                            name=formatted_row[1],
                            birth=formatted_row[2],
                            year=formatted_row[3],
                            month=formatted_row[4],
                            day=formatted_row[5],
                            age=age,
                            email=formatted_row[7],
                            gender=formatted_row[8],
                            male=formatted_row[9],
                            female=formatted_row[10],
                            phone=formatted_row[11],
                            address=formatted_row[12],
                            consultation_start=formatted_row[13],
                            start_year=formatted_row[14],
                            start_month=formatted_row[15],
                            start_day=formatted_row[16],
                            consultation_end=formatted_row[17],
                            end_year=formatted_row[18],
                            end_month=formatted_row[19],
                            end_day=formatted_row[20],
                            issue=formatted_row[21],
                            sessions=formatted_row[22],
                            notes=formatted_row[23]
                        )
    
    rows = sql.read_users(search_query)  # 검색 쿼리를 전달
    
    for row in rows:
        formatted_row = list(row)
        for i, header in enumerate(headers):
            value = row[i]
            if isinstance(value, str):
                formatted_row[i] = value
            elif isinstance(value, int):
                formatted_row[i] = str(value)
        
        # headers 리스트에서 viewonly_headers에 해당하는 항목의 인덱스하여 selected_column에 저장
        indices = [headers.index(header) for header in viewonly_headers]
        selected_column = [formatted_row[i] for i in indices]

        treeview_users.insert("", tk.END, iid=str(row[0]), values=selected_column)
        
    # 메뉴바 생성
    main_widgets = [entry_search, button_search, button_show_all, button_create, button_update, button_delete, export_button]
    
    settings = load_settings()
    update_font_size(settings["font_size"], main_widgets)

    create_menu(root, main_widgets)

def on_user_select(event=None):
    selected_item = treeview_users.selection()
    if selected_item:
        user_id = selected_item[0]
        open_update_window(user_id)

def delete_user_gui():
    selected_item = treeview_users.selection()
    if selected_item:
        user_id = selected_item[0]
        user_data = treeview_users.item(selected_item, 'values')
        user_name = user_data[0]
        
        confirm = messagebox.askyesno("리스트 삭제", f"'{user_name}'을 삭제하시겠습니까?")
        
        if confirm:
            sql.delete_user(user_id)
            messagebox.showinfo("삭제 완료", "리스트가 삭제되었습니다.")
            read_users_gui()
    else:
        messagebox.showwarning("Selection Error", "Please select a user from the list.")

def search_users(event=None):
    search_field = search_field_var.get()
    search_value = entry_search.get()
    search_query = {search_field: search_value}
    read_users_gui(search_query)

def show_all_users():
    entry_search.delete(0, tk.END)  # 검색 입력 필드 비우기
    read_users_gui()  # 전체 목록 불러오기

def export_to_excel(user_id=None):
    """현재 데이터를 엑셀 파일로 내보내는 함수"""
    if user_id is None:
        data = sql.fetch_users()  # 데이터베이스에서 고객 데이터 가져오기
        file_name = "고객_목록.xlsx"
        columns_list = viewonly_headers
        messagebox.showinfo("정보", "고객 목록 엑셀 파일로 내보내졌습니다.")
    else:
        data = sql.fetch_users_by_id(user_id)  # 데이터베이스에서 고객 데이터 가져오기
        user_name = sql.fetch_user_name_by_id(user_id)
        file_name = user_name + "_정보.xlsx"
        columns_list = export_headers
        messagebox.showinfo("정보", user_name + "님 정보가 엑셀 파일로 내보내졌습니다.")
    
    df = pd.DataFrame(data, columns=columns_list)
    df.to_excel(file_name, index=False, engine='openpyxl')

def save_settings(settings, filename="settings.json"):
    with open(filename, "w") as f:
        json.dump(settings, f)

def load_settings(filename="settings.json"):
    try:
        with open(filename, "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        # 기본 설정을 반환 (파일이 없을 경우)
        settings = {"font_size": 100}
    return settings

def on_closing():
    save_settings(settings)
    root.destroy()

search_frame = tk.Frame(root)
search_frame.grid(row=0, column=0, columnspan=5, pady=1, sticky='w')  # 상단 좌측에 배치

# 검색 필드 및 드롭다운 메뉴 설정
label_search = tk.Label(search_frame, text="분류")
label_search.grid(row=0, column=0, padx=10, pady=10, sticky='e')

search_field_var = tk.StringVar(value="이름")  # 기본 검색 필드를 이름으로 설정

# 드롭다운 메뉴 (Combobox)로 필드 선택
option_menu = ttk.Combobox(search_frame, textvariable=search_field_var, values=viewonly_headers, width=20)
option_menu.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# 검색 입력 필드
entry_search = tk.Entry(search_frame, width=30)
entry_search.grid(row=0, column=2, padx=10, pady=10, sticky='w')

# 검색 버튼
button_search = tk.Button(search_frame, text="검색", command=search_users)
button_search.grid(row=0, column=3, padx=10, pady=10, sticky='w')

# 전체 목록 보기 버튼
button_show_all = tk.Button(search_frame, text="전체 보기", command=show_all_users)
button_show_all.grid(row=0, column=4, padx=10, pady=10, sticky='w')

# 버튼들을 1행으로 배치하기 위한 Frame 사용
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=5, pady=1, sticky='e')  # 상단 우측에 배치

button_create = tk.Button(button_frame, text="신규 생성", command=open_create_user_window)
button_create.grid(row=0, column=0, padx=10)

button_update = tk.Button(button_frame, text="편집", command=on_user_select)
button_update.grid(row=0, column=1, padx=10)

button_delete = tk.Button(button_frame, text="삭제", command=delete_user_gui)
button_delete.grid(row=0, column=2, padx=10)

export_button = tk.Button(button_frame, text="목록 출력", command=export_to_excel)
export_button.grid(row=0, column=3, padx=5, pady=5)

# Bind the Enter key to the search_users function
entry_search.bind("<Return>", search_users)

# Grid 레이아웃의 행과 열 비율 조정
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(2, weight=1)

# Treeview의 더블 클릭 이벤트 바인딩
treeview_users.bind("<Double-1>", on_user_select)

# 시작 시 사용자 목록 읽기
read_users_gui()

# config 저장
root.protocol("WM_DELETE_WINDOW", on_closing)

# GUI 루프 시작
root.mainloop()

# 프로그램 종료 시 데이터베이스 연결 종료
sql.close_connection()
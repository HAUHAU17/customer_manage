import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font
from tkcalendar import DateEntry
import sql  # sql.py 파일을 import
from datetime import datetime
import pandas as pd

# GUI 애플리케이션 생성
root = tk.Tk()
root.title("고객 관리 프로그램")
root.geometry("1400x800")  # 메인 창 초기 크기 설정

# 기본 폰트 크기
BASE_FONT_SIZE = 10
custom_font = font.Font(size=BASE_FONT_SIZE)

# Treeview 설정
headers = [
    "ID", "이름", "생년월일", "년", "월", "일", "나이", "메일", "성별", "남자", "여자", "전화번호", "주소", "상담시작일", "상담종료일", "호소문제-1", "호소문제-2", "회기 수", "특이사항"
]
viewonly_headers = [
    "ID", "이름", "생년월일", "나이", "메일", "성별", "전화번호", "주소", "상담시작일", "상담종료일", "회기 수"
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
    global custom_font
    custom_font = font.Font(size=size)

    # 적용할 위젯 리스트
    for widget in all_widgets:
        widget.config(font=custom_font)
    
    # Treeview의 스타일 업데이트
    style = ttk.Style()
    style.configure("Treeview", font=custom_font)

def set_font_size(percent, all_widgets):
    update_font_size(percent, all_widgets)

def create_menu(root, all_widgets):
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    
    font_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="글씨 크기", menu=font_menu)
    
    # 퍼센트 항목 추가
    percent_buttons = [100, 110, 120, 130, 140, 150]
    for percent in percent_buttons:
        font_menu.add_command(label=f"{percent}%", command=lambda p=percent: set_font_size(p, all_widgets))

def validate_integer(input_value):
    """정수만 허용하는 검증 함수"""
    return input_value.isdigit() or input_value == ""

def validate_phone(input_value):
    """전화번호에 숫자와 공백만 허용하는 검증 함수"""
    return all(char.isdigit() or char.isspace() for char in input_value) or input_value == ""

def validate_hyphen(input_value):
    """"-"만 허용하는 검증 함수"""
    return  input_value!="-"

def create_field_entries(window):
    """필드 및 라벨 설정을 함수화하여 중복 제거."""
    labels_and_fields = {}
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
        if header in ["회기 수"]:
            entry = tk.Entry(window, width=10, validate="key", validatecommand=(window.register(validate_integer), "%P"))
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
        elif header in ["상담시작일", "상담종료일"]:
            entry = DateEntry(window, width=10, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        elif header in ["특이사항"]:
            entry = tk.Text(window, height=10, width=60)
        elif header in ["메일"]:
            entry = tk.Entry(window, width=30, validate="key", validatecommand=(window.register(validate_hyphen), "%P"))
        elif header in ["주소", "호소문제-1", "호소문제-2"]:
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
    create_menu(window, window_widgets)  # Pass the widget list to create_menu

    return labels_and_fields

def grid_field_entries(labels_and_fields, window):
    """필드 및 라벨의 그리드를 설정."""
    row = 0
    for label_text, entry in labels_and_fields.items():
        if label_text == "생년월일" or label_text == "성별":
            # Handling the special case for "생년월일", "성별"
            tk.Label(window, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky='ew')
        elif label_text == "년":
            entry.grid(row=row, column=1, padx=1, pady=5, sticky='w')
            tk.Label(window, text=label_text).grid(row=row, column=2, padx=1, pady=5, sticky='w')
        elif label_text == "월":
            entry.grid(row=row, column=3, padx=1, pady=5, sticky='w')
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
        else:
            tk.Label(window, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky='ew')
            if label_text == "이름" or label_text == "나이" or label_text == "회기 수":
                entry.grid(row=row, column=1, padx=1, pady=5, sticky='w')
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
        if label in ["상담시작일", "상담종료일"]:
            date_str = user_data[index]
            if date_str:
                entry.set_date(datetime.strptime(date_str, '%Y-%m-%d'))  # DateEntry에 날짜 설정
        else:
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
        # 날짜 형식으로 변환
        consultation_start = values.get("상담시작일", "").strftime('%Y-%m-%d') if isinstance(values.get("상담시작일"), datetime) else values.get("상담시작일", "")
        consultation_end = values.get("상담종료일", "").strftime('%Y-%m-%d') if isinstance(values.get("상담종료일"), datetime) else values.get("상담종료일", "")
        
        # 생년월일 병합
        today = datetime.today()
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
                    consultation_end=consultation_end,
                    issue_1=values.get("호소문제-1", "") or "-",
                    issue_2=values.get("호소문제-2", "") or "-",
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
                    consultation_end=consultation_end,
                    issue_1=values.get("호소문제-1", "") or "-",
                    issue_2=values.get("호소문제-2", "") or "-",
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

    entries = create_field_entries(create_window)
    grid_field_entries(entries, create_window)

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
    button_save.grid(row=len(headers), column=10, padx=5, pady=5)

def open_update_window(user_id):
    user_data = [row for row in sql.read_users() if str(row[0]) == user_id][0]
    update_window = tk.Toplevel(root)
    update_window.title("편집")
    update_window.geometry("800x600")  # 새 창 크기 설정

    entries = create_field_entries(update_window)
    grid_field_entries(entries, update_window)

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
    button_export.grid(row=len(headers), column=9, padx=5, pady=5)

    button_save = tk.Button(update_window, text="저장", command=save_updates)
    button_save.grid(row=len(headers), column=10, padx=5, pady=5)

def read_users_gui(search_query=None):
    treeview_users.delete(*treeview_users.get_children())
    rows = sql.read_users(search_query)  # 검색 쿼리를 전달
    for row in rows:
        formatted_row = list(row)
        for i, header in enumerate(headers):
            if header in ["상담시작일", "상담종료일"]:
                value = row[i]
                if isinstance(value, str):
                    formatted_row[i] = value  # 문자열인 경우 그대로 사용
                elif isinstance(value, int):
                    # int를 datetime으로 변환
                    date_str = str(value)
                    if len(date_str) == 8:  # YYYYMMDD
                        formatted_date = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')
                        formatted_row[i] = formatted_date
                    else:
                        formatted_row[i] = ""  # 유효하지 않은 형식
                else:
                    # datetime 객체인 경우
                    formatted_row[i] = value.strftime('%Y-%m-%d') if value else ""
        
        # headers 리스트에서 viewonly_headers에 해당하는 항목의 인덱스하여 selected_column에 저장
        indices = [headers.index(header) for header in viewonly_headers]
        selected_column = [formatted_row[i] for i in indices]
        
        treeview_users.insert("", tk.END, iid=str(row[0]), values=selected_column)
        
    # 메뉴바 생성
    main_widgets = [entry_search, button_search, button_show_all, button_create, button_update, button_delete, export_button]
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
    else:
        data = sql.fetch_users_by_id(user_id)  # 데이터베이스에서 고객 데이터 가져오기
        user_name = sql.fetch_user_name_by_id(user_id)
        file_name = user_name + "_정보.xlsx"
    
    df = pd.DataFrame(data, columns=headers)
    df.to_excel(file_name, index=False, engine='openpyxl')
    messagebox.showinfo("정보", "데이터가 엑셀 파일로 내보내졌습니다.")

# 검색 필드 및 드롭다운 메뉴 설정
label_search = tk.Label(root, text="분류")
label_search.grid(row=0, column=0, padx=10, pady=10, sticky='e')

search_field_var = tk.StringVar(value="이름")  # 기본 검색 필드를 이름으로 설정

# 드롭다운 메뉴 (Combobox)로 필드 선택
option_menu = ttk.Combobox(root, textvariable=search_field_var, values=headers, width=20)
option_menu.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# 검색 입력 필드
entry_search = tk.Entry(root, width=30)
entry_search.grid(row=0, column=2, padx=10, pady=10, sticky='w')

# 검색 버튼
button_search = tk.Button(root, text="검색", command=search_users)
button_search.grid(row=0, column=3, padx=10, pady=10, sticky='w')

# 전체 목록 보기 버튼
button_show_all = tk.Button(root, text="전체 보기", command=show_all_users)
button_show_all.grid(row=0, column=4, padx=10, pady=10, sticky='w')

# 버튼들을 1행으로 배치하기 위한 Frame 사용
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=5, pady=10, sticky='e')  # 상단 우측에 배치

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

# GUI 루프 시작
root.mainloop()

# 프로그램 종료 시 데이터베이스 연결 종료
sql.close_connection()
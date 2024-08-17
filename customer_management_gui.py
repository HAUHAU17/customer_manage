import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry 

# Database interaction functions (imported from another module)
from sql import add_customer, get_customers, delete_customer, update_customer, close_connection, get_customer_by_id



def calculate_age(year, month, day):
    birthdate = datetime(year, month, day)
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def save_customer():
    name = entry_name.get()
    birth_year = entry_birth_year.get()
    birth_month = entry_birth_month.get()
    birth_day = entry_birth_day.get()
    age = entry_age.get()
    
    # 핸드폰 번호를 3부분으로 나누어 입력받기
    phone_part1 = entry_phone1.get()
    phone_part2 = entry_phone2.get()
    phone_part3 = entry_phone3.get()
    
    # 핸드폰 번호를 전체 문자열로 결합
    phone = f"{phone_part1}-{phone_part2}-{phone_part3}"
    
    email = entry_email.get()
    address = entry_address.get()
    gender = gender_var.get()
    session_start_date = entry_session_start.get()
    session_end_date = entry_session_end.get()
    presenting_problem = entry_presenting_problem.get("1.0", tk.END).strip()
    session_count = entry_session_count.get()
    special_notes = entry_special_notes.get("1.0", tk.END).strip()

    # 고객 추가 함수 호출
    add_customer(name, birth_year, birth_month, birth_day, age, phone, email, address, gender,
                 session_start_date, session_end_date, presenting_problem, session_count, special_notes)

    messagebox.showinfo("저장 완료", "고객 정보가 저장되었습니다.")
    clear_entries()
    load_customers()
    notebook.select(tab_all_customers) 


def clear_entries():
    entry_name.delete(0, tk.END)
    entry_birth_year.delete(0, tk.END)
    entry_birth_month.delete(0, tk.END)
    entry_birth_day.delete(0, tk.END)
    entry_phone1.delete(0, tk.END)
    entry_phone2.delete(0, tk.END)
    entry_phone3.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    gender_var.set('남')
    entry_session_start.set_date(datetime.today())
    entry_session_end.set_date(datetime.today())
    entry_presenting_problem.delete("1.0", tk.END)
    entry_session_count.delete(0, tk.END)
    entry_special_notes.delete("1.0", tk.END)

def load_customers(query=""):
    customers = get_customers(query)
    treeview_customers.delete(*treeview_customers.get_children())
    for customer in customers:
        # Combine birth year, month, and day into a single string for display
        birthdate = f"{customer[2]}-{customer[3]:02d}-{customer[4]:02d}"
        treeview_customers.insert('', tk.END, values=(customer[0], customer[1], birthdate, customer[5],
                                                      customer[6], customer[7], customer[8], customer[9],
                                                      customer[10], customer[11], customer[12], customer[13]))



def delete_selected_customer():
    selected_item = treeview_customers.selection()
    if selected_item:
        customer_id = treeview_customers.item(selected_item)['values'][0]
        delete_customer(customer_id)
        load_customers()

def show_customer_info(event):
    selected_item = treeview_customers.selection()
    if selected_item:
        customer_values = treeview_customers.item(selected_item)['values']
        if len(customer_values) >= 1:  # ID를 가져오는 경우, 최소 1개 값이 있어야 합니다.
            customer_id = customer_values[0]  # ID를 올바르게 추출합니다.

            # 모든 정보 가져오기
            all_info = get_customer_by_id(customer_id)
            if all_info:
                # 반환값의 수에 맞게 변수에 저장합니다.
                (id, name, birth_year, birth_month, birth_day, age, phone, email, address, gender,
                 session_start_date, session_end_date, presenting_problem, session_count, special_notes) = all_info

                # 탭 생성
                create_customer_tab(customer_id, name, phone, email, address, gender,
                                    session_start_date, session_end_date, presenting_problem,
                                    session_count, special_notes, birth_year, birth_month, birth_day, age)




def search_customers(event=None):
    search_term = entry_search.get()
    load_customers(search_term)

tab_names = {}
def create_customer_tab(customer_id, name, phone, email, address, gender,
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
    tk.Label(new_tab, text="나이:").grid(row=6, column=3, padx=10, pady=5, sticky="w")  # 나이 라벨 추가
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
    entry_age_edit.grid(row=6, column=4, padx=10, pady=5)
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
    entry_presenting_problem.insert("1.0", presenting_problem)

    entry_session_count = tk.Entry(new_tab)
    entry_session_count.grid(row=10, column=1, padx=10, pady=5, sticky="ew")
    entry_session_count.insert(0, session_count)

    entry_special_notes = tk.Text(new_tab, height=4, width=40)
    entry_special_notes.grid(row=11, column=1, padx=10, pady=5, sticky="ew", columnspan=4)
    entry_special_notes.insert("1.0", special_notes)

    def save_edits():
        updated_name = entry_name_edit.get()
        updated_phone = f"{entry_phone1_edit.get()}-{entry_phone2_edit.get()}-{entry_phone3_edit.get()}" 
        updated_email = entry_email_edit.get()
        updated_address = entry_address_edit.get()
        updated_gender = gender_var.get()
        updated_session_start = entry_session_start.get_date().strftime('%Y-%m-%d')
        updated_session_end = entry_session_end.get_date().strftime('%Y-%m-%d')
        updated_presenting_problem = entry_presenting_problem.get("1.0", tk.END).strip()
        updated_session_count = entry_session_count.get()
        updated_special_notes = entry_special_notes.get("1.0", tk.END).strip()
        
        # 생년월일을 연도, 월, 일로 조합
        updated_birth_year = entry_birth_year.get()
        updated_birth_month = entry_birth_month.get()
        updated_birth_day = entry_birth_day.get()
        updated_birthdate = f"{updated_birth_year}-{int(updated_birth_month):02d}-{int(updated_birth_day):02d}"
        updated_age = entry_age_edit.get()

        # Update customer information using ID
        update_customer(customer_id, updated_name, updated_phone, updated_email, updated_address,
                        updated_gender, updated_session_start, updated_session_end,
                        updated_presenting_problem, updated_session_count, updated_special_notes,
                        updated_birthdate, updated_age)
        messagebox.showinfo("저장 완료", "저장되었습니다.")
        load_customers()  # Refresh the customer list
        tab_names.pop(name, None)  # Remove old tab reference
        tab_names[updated_name] = new_tab  # Add updated tab reference
        notebook.tab(new_tab, text=f"{updated_name} [x]")  # Update tab name


        notebook.select(tab_all_customers) 

    save_button_edit = tk.Button(new_tab, text="저장", command=save_edits)
    save_button_edit.grid(row=10, column=1, pady=10)

    def delete_customer_info():
        if messagebox.askyesno("삭제 확인", "정말로 삭제하시겠습니까?"):
            delete_customer(customer_id)
            load_customers()
            close_tab(tab_name, new_tab)
            notebook.select(tab_all_customers) 

    delete_button_edit = tk.Button(new_tab, text="삭제", command=delete_customer_info)
    delete_button_edit.grid(row=10, column=2, pady=10)

    # Update the tab_names dictionary
    tab_names[tab_name] = new_tab


def close_tab(tab_name, tab_frame):
    if tab_name in tab_names:
        notebook.forget(tab_names[tab_name])  # Remove the tab from notebook
        tab_names.pop(tab_name, None)  # Remove tab from the dictionary
        tab_frame.destroy()  # Explicitly destroy the tab frame
    notebook.select(tab_all_customers)

def show_all_customers():
    load_customers()

root = tk.Tk()
root.title("고객 관리 프로그램")
root.geometry("800x600")  # Set default window size

# Create and place the X button at the window's top-right corner
def close_app():
    close_connection()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_app)

notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both")

# 첫 번째 탭: 전체 고객
tab_all_customers = ttk.Frame(notebook)
notebook.add(tab_all_customers, text="전체 고객", sticky="nsew")

frame_search = tk.Frame(tab_all_customers)
frame_search.pack(padx=10, pady=10, fill="x")

entry_search = tk.Entry(frame_search)
entry_search.pack(side="left", fill="x", expand=True)

search_button = tk.Button(frame_search, text="찾기", command=search_customers)
search_button.pack(side="left", padx=10)

view_all_button = tk.Button(frame_search, text="전체보기", command=show_all_customers)
view_all_button.pack(side="left")

# Treeview for displaying customers
treeview_customers = ttk.Treeview(tab_all_customers, columns=("ID", "Name", "Birthdate", "Age", "Phone", "Email", "Address", "Gender", "Session Start", "Session End", "Presenting Problem", "Session Count", "Special Notes"), show='headings')
treeview_customers.heading("ID", text="ID")
treeview_customers.heading("Name", text="이름")
treeview_customers.heading("Birthdate", text="생년월일")
treeview_customers.heading("Age", text="나이")
treeview_customers.heading("Phone", text="전화번호")
treeview_customers.heading("Email", text="이메일")
treeview_customers.heading("Address", text="주소")
treeview_customers.heading("Gender", text="성별")
treeview_customers.heading("Session Start", text="상담 시작일")
treeview_customers.heading("Session End", text="상담 종료일")
treeview_customers.heading("Session Count", text="회기수")
treeview_customers.heading("Special Notes", text="특이사항")

treeview_customers.column("ID", width=50, anchor="w")
treeview_customers.column("Name", width=150, anchor="w")
treeview_customers.column("Birthdate", width=100, anchor="w")
treeview_customers.column("Age", width=50, anchor="w")
treeview_customers.column("Phone", width=150, anchor="w")
treeview_customers.column("Email", width=150, anchor="w")
treeview_customers.column("Address", width=200, anchor="w")
treeview_customers.column("Gender", width=80, anchor="w")
treeview_customers.column("Session Start", width=100, anchor="w")
treeview_customers.column("Session End", width=100, anchor="w")
treeview_customers.column("Presenting Problem", width=200, anchor="w")
treeview_customers.column("Session Count", width=80, anchor="w")
treeview_customers.column("Special Notes", width=200, anchor="w")

treeview_customers.pack(padx=10, pady=10, fill="both", expand=True)
treeview_customers.bind("<Double-1>", show_customer_info)

load_customers()

# 두 번째 탭: 고객 추가
tab_add_customer = ttk.Frame(notebook)
notebook.add(tab_add_customer, text="고객 추가")

# 생년월일 및 나이 계산
def update_age(*args):
    try:
        birth_year = int(entry_birth_year.get())
        birth_month = int(entry_birth_month.get())
        birth_day = int(entry_birth_day.get())
        age = calculate_age(birth_year, birth_month, birth_day)
        entry_age.config(state='normal')
        entry_age.delete(0, tk.END)
        entry_age.insert(0, str(age))
        entry_age.config(state='readonly')
    except ValueError:
        pass  # 값이 입력되기 전에 발생하는 오류를 무시

# 이름 입력
tk.Label(tab_add_customer, text="이름:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_name = tk.Entry(tab_add_customer)
entry_name.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

# 성별 입력
tk.Label(tab_add_customer, text="성별:").grid(row=0, column=2, padx=10, pady=5, sticky="w")
gender_var = tk.StringVar(value='남')
gender_male_rb = tk.Radiobutton(tab_add_customer, text="남", variable=gender_var, value='남')
gender_female_rb = tk.Radiobutton(tab_add_customer, text="여", variable=gender_var, value='여')
gender_male_rb.grid(row=0, column=3, padx=10, pady=5, sticky="w")
gender_female_rb.grid(row=0, column=4, padx=10, pady=5, sticky="w")

# 생년월일 입력
tk.Label(tab_add_customer, text="생년월일:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
tk.Label(tab_add_customer, text="년:").grid(row=1, column=2, padx=2, pady=5, sticky="w")
entry_birth_year = tk.Entry(tab_add_customer, width=5)
entry_birth_year.grid(row=1, column=1, padx=10, pady=5, sticky="w")

tk.Label(tab_add_customer, text="월:").grid(row=1, column=4, padx=2, pady=5, sticky="w")
entry_birth_month = tk.Entry(tab_add_customer, width=3)
entry_birth_month.grid(row=1, column=3, padx=10, pady=5, sticky="w")

tk.Label(tab_add_customer, text="일:").grid(row=1, column=6, padx=2, pady=5, sticky="w")
entry_birth_day = tk.Entry(tab_add_customer, width=3)
entry_birth_day.grid(row=1, column=5, padx=10, pady=5, sticky="w")

# 나이 표시 (읽기 전용)
tk.Label(tab_add_customer, text="나이:").grid(row=1, column=7, padx=10, pady=5, sticky="w")
entry_age = tk.Entry(tab_add_customer, state="readonly")
entry_age.grid(row=1, column=8, padx=10, pady=5, sticky="ew")

entry_birth_year.bind("<KeyRelease>", update_age)
entry_birth_month.bind("<KeyRelease>", update_age)
entry_birth_day.bind("<KeyRelease>", update_age)

# 전화번호 입력
tk.Label(tab_add_customer, text="전화번호:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_phone1 = tk.Entry(tab_add_customer, width=5)
entry_phone1.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
tk.Label(tab_add_customer, text="-").grid(row=2, column=2, padx=0, pady=5)
entry_phone2 = tk.Entry(tab_add_customer, width=10)
entry_phone2.grid(row=2, column=3, padx=0, pady=5, sticky="ew")
tk.Label(tab_add_customer, text="-").grid(row=2, column=4, padx=0, pady=5)
entry_phone3 = tk.Entry(tab_add_customer, width=10)
entry_phone3.grid(row=2, column=5, padx=0, pady=5, sticky="ew")

# 이메일 입력
tk.Label(tab_add_customer, text="이메일:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_email = tk.Entry(tab_add_customer)
entry_email.grid(row=3, column=1, padx=10, pady=5, sticky="ew", columnspan=4)

# 주소 입력
tk.Label(tab_add_customer, text="주소:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_address = tk.Entry(tab_add_customer)
entry_address.grid(row=4, column=1, padx=10, pady=5, sticky="ew", columnspan=4)

# 상담 시작일 입력
tk.Label(tab_add_customer, text="상담 시작일:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
entry_session_start = DateEntry(tab_add_customer, date_pattern='yyyy-mm-dd')
entry_session_start.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

# 상담 종결일 입력
tk.Label(tab_add_customer, text="상담 종결일:").grid(row=5, column=2, padx=10, pady=5, sticky="w")
entry_session_end = DateEntry(tab_add_customer, date_pattern='yyyy-mm-dd')
entry_session_end.grid(row=5, column=3, padx=10, pady=5, sticky="ew")

# 호소 문제 입력
tk.Label(tab_add_customer, text="호소 문제:").grid(row=6, column=0, padx=10, pady=5, sticky="nw")
entry_presenting_problem = tk.Text(tab_add_customer, height=4, width=40)
entry_presenting_problem.grid(row=6, column=1, padx=10, pady=5, sticky="ew", columnspan=4)

# 회기수 입력
tk.Label(tab_add_customer, text="회기수:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
entry_session_count = tk.Entry(tab_add_customer)
entry_session_count.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

# 특이사항 입력
tk.Label(tab_add_customer, text="특이사항:").grid(row=8, column=0, padx=10, pady=5, sticky="nw")
entry_special_notes = tk.Text(tab_add_customer, height=4, width=40)
entry_special_notes.grid(row=8, column=1, padx=10, pady=5, sticky="ew", columnspan=4)

# 저장 버튼
save_button = tk.Button(tab_add_customer, text="저장", command=save_customer)
save_button.grid(row=9, column=1, padx=10, pady=10, columnspan=4, sticky="e")

# Make sure columns expand
tab_add_customer.grid_columnconfigure(1, weight=1)
tab_add_customer.grid_columnconfigure(3, weight=1)
tab_add_customer.grid_columnconfigure(4, weight=1)
tab_add_customer.grid_columnconfigure(5, weight=1)

load_customers()

root.mainloop()

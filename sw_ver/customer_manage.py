import tkinter as tk
from tkinter import messagebox, ttk
import sql  # sql.py 파일을 import

# GUI 애플리케이션 생성
root = tk.Tk()
root.title("User Management")
root.geometry("800x600")  # 메인 창 초기 크기 설정

def open_create_user_window():
    create_window = tk.Toplevel(root)
    create_window.title("Create New User")
    create_window.geometry("400x300")  # 새 창 크기 설정

    label_name = tk.Label(create_window, text="Name")
    label_name.pack(pady=10)
    entry_name = tk.Entry(create_window, width=40)
    entry_name.pack(pady=5)

    label_age = tk.Label(create_window, text="Age")
    label_age.pack(pady=10)
    
    # Validate command to ensure only integer values are entered
    validate_age = create_window.register(lambda input: input.isdigit() or input == "") 
    entry_age = tk.Entry(create_window, width=40, validate="key", validatecommand=(validate_age, "%P"))
    entry_age.pack(pady=5)

    entry_name.focus_set()  # 새 창 열릴 때 Name 입력 필드에 포커스

    def save_new_user():
        name = entry_name.get()
        age = entry_age.get()
        if name and age.isdigit():
            sql.create_user(name, age)
            messagebox.showinfo("Success", "User added!")
            read_users_gui()
            create_window.destroy()  # 창 닫기
        else:
            messagebox.showwarning("Input Error", "Please enter a valid name and age (integer).")

    button_save = tk.Button(create_window, text="Save", command=save_new_user)
    button_save.pack(pady=10)

def read_users_gui(search_query=None):
    treeview_users.delete(*treeview_users.get_children())
    rows = sql.read_users(search_query)  # 검색 쿼리를 전달
    for row in rows:
        treeview_users.insert("", tk.END, values=(row[1], row[2]))  # 이름과 나이만 표시

def on_user_select(event):
    selected_item = treeview_users.selection()
    if selected_item:
        user_data = treeview_users.item(selected_item, 'values')
        print(f"Selected user data: {user_data}")  # 디버깅을 위한 출력
        
        # 사용자의 ID를 찾기 위한 수정된 방법
        try:
            user_id = next(row[0] for row in sql.read_users() if row[1] == user_data[0] and row[2] == user_data[1])
            open_update_window(user_id)
        except StopIteration:
            messagebox.showerror("Selection Error", "Selected user data does not match any records.")

def open_update_window(user_id):
    user_data = [row for row in sql.read_users() if row[0] == user_id][0]
    update_window = tk.Toplevel(root)
    update_window.title("Update User")
    update_window.geometry("400x300")  # 새 창 크기 설정

    label_name = tk.Label(update_window, text="Name")
    label_name.pack(pady=10)
    entry_name = tk.Entry(update_window, width=40)
    entry_name.pack(pady=5)
    entry_name.insert(0, user_data[1])  # 기존 이름 삽입

    label_age = tk.Label(update_window, text="Age")
    label_age.pack(pady=10)
    
    # Validate command to ensure only integer values are entered
    validate_age = update_window.register(lambda input: input.isdigit() or input == "") 
    entry_age = tk.Entry(update_window, width=40, validate="key", validatecommand=(validate_age, "%P"))
    entry_age.pack(pady=5)
    entry_age.insert(0, user_data[2])  # 기존 나이 삽입

    entry_name.focus_set()  # 새 창 열릴 때 Name 입력 필드에 포커스

    def save_updates():
        new_name = entry_name.get()
        new_age = entry_age.get()
        if new_name and new_age.isdigit():
            sql.update_user(user_id, new_name, new_age)
            messagebox.showinfo("Success", "User updated!")
            read_users_gui()
            update_window.destroy()  # 창 닫기
        else:
            messagebox.showwarning("Input Error", "Please enter a valid name and age (integer).")

    button_save = tk.Button(update_window, text="Save", command=save_updates)
    button_save.pack(pady=10)

def update_user_gui():
    on_user_select(None)  # 선택된 사용자 없을 경우 업데이트 창을 열 수 있도록 수정

def delete_user_gui():
    selected_item = treeview_users.selection()
    if selected_item:
        user_data = treeview_users.item(selected_item, 'values')
        user_id = [row[0] for row in sql.read_users() if row[1] == user_data[0] and row[2] == user_data[1]][0]
        user_name = user_data[0]
        
        # 삭제 확인 메시지 박스
        confirm = messagebox.askyesno("Delete Confirmation", f"Are you sure you want to delete user '{user_name}'?")
        
        if confirm:
            sql.delete_user(user_id)
            messagebox.showinfo("Success", "User deleted!")
            read_users_gui()
    else:
        messagebox.showwarning("Selection Error", "Please select a user from the list.")

def search_users():
    search_field = search_field_var.get()
    search_value = entry_search.get()
    search_query = {search_field: search_value}
    read_users_gui(search_query)

def show_all_users():
    entry_search.delete(0, tk.END)  # 검색 입력 필드 비우기
    read_users_gui()  # 전체 목록 불러오기

# GUI 위젯 설정
label_search = tk.Label(root, text="Search by")
label_search.grid(row=0, column=0, padx=10, pady=10, sticky='w')

search_field_var = tk.StringVar(value="name")  # 기본 검색 필드를 이름으로 설정

# 드롭다운 메뉴 (Combobox)로 필드 선택
option_menu = ttk.Combobox(root, textvariable=search_field_var, values=["name", "age"], width=20)
option_menu.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# 검색 입력 필드
entry_search = tk.Entry(root, width=30)
entry_search.grid(row=0, column=2, padx=10, pady=10, sticky='w')

# 검색 버튼
button_search = tk.Button(root, text="Search", command=search_users)
button_search.grid(row=0, column=3, padx=10, pady=10, sticky='w')

# 전체 목록 보기 버튼
button_show_all = tk.Button(root, text="Show All Users", command=show_all_users)
button_show_all.grid(row=0, column=4, padx=10, pady=10, sticky='w')

# 버튼들을 1행으로 배치하기 위한 Frame 사용
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=5, pady=10, sticky='e')  # 상단 우측에 배치

button_create = tk.Button(button_frame, text="Create User", command=open_create_user_window)
button_create.grid(row=0, column=0, padx=10)

button_update = tk.Button(button_frame, text="Update User", command=update_user_gui)
button_update.grid(row=0, column=1, padx=10)

button_delete = tk.Button(button_frame, text="Delete User", command=delete_user_gui)
button_delete.grid(row=0, column=2, padx=10)

# Treeview 설정
treeview_users = ttk.Treeview(root, columns=("Name", "Age"), show='headings')
treeview_users.heading("Name", text="Name")
treeview_users.heading("Age", text="Age")
treeview_users.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')
treeview_users.bind("<Double-1>", on_user_select)  # 더블 클릭 이벤트 바인딩

# Grid 레이아웃의 행과 열 비율 조정
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(2, weight=1)

# 시작 시 사용자 목록 읽기
read_users_gui()

# GUI 루프 시작
root.mainloop()

# 프로그램 종료 시 데이터베이스 연결 종료
sql.close_connection()
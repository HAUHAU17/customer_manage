import tkinter as tk
from tkinter import ttk, messagebox
from sql import add_customer, get_customers, delete_customer, update_customer, close_connection, get_customer_by_id, get_customer_id_by_info

def save_customer():
    name = entry_name.get()
    phone = f"{entry_phone1.get()}-{entry_phone2.get()}-{entry_phone3.get()}"
    email = entry_email.get()
    address = entry_address.get()
    
    # 고객 추가
    add_customer(name, phone, email, address)
    messagebox.showinfo("저장 완료", "저장되었습니다.")
    entry_name.delete(0, tk.END)
    entry_phone1.delete(0, tk.END)
    entry_phone2.delete(0, tk.END)
    entry_phone3.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    load_customers()

def load_customers(query=""):
    customers = get_customers(query)
    treeview_customers.delete(*treeview_customers.get_children())
    for customer in customers:
        # Ensure the order is (id, name, phone, email, address)
        treeview_customers.insert('', tk.END, values=(customer[0], customer[1], customer[2], customer[3], customer[4]))

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
        if len(customer_values) >= 5:
            customer_id = customer_values[0]  # ID를 올바르게 추출합니다.
            name = customer_values[1]
            phone = customer_values[2]
            email = customer_values[3]
            address = customer_values[4]  # 올바른 인덱스 사용
            create_customer_tab(customer_id, name, phone, email, address)

def search_customers(event=None):
    search_term = entry_search.get()
    load_customers(search_term)

def create_customer_tab(customer_id, name, phone, email, address):
    tab_name = name

    if tab_name in tab_names:
        notebook.select(tab_names[tab_name])
        return

    new_tab = ttk.Frame(notebook)

    # Add the tab to the notebook
    notebook.add(new_tab, text=f"{tab_name} [x]", sticky="nsew")

    # Add X button to the tab frame
    close_button = tk.Button(new_tab, text="X", command=lambda: close_tab(tab_name, new_tab))
    close_button.grid(row=0, column=1, padx=5, pady=5, sticky='ne')

    # Customer info display and editing
    tk.Label(new_tab, text="이름:").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(new_tab, text="전화번호:").grid(row=2, column=0, padx=10, pady=5)
    
    phone_validate = root.register(lambda input: input.isdigit() or input == '')  # 숫자만 허용하는 validation 함수

    entry_phone1_edit = tk.Entry(new_tab, validate="key", validatecommand=(phone_validate, '%P'), width=5)
    entry_phone1_edit.grid(row=2, column=1, padx=10, pady=5)
    entry_phone1_edit.insert(0, phone.split('-')[0])

    tk.Label(new_tab, text="-").grid(row=2, column=2, padx=0, pady=5)

    entry_phone2_edit = tk.Entry(new_tab, validate="key", validatecommand=(phone_validate, '%P'), width=4)
    entry_phone2_edit.grid(row=2, column=3, padx=0, pady=5)
    entry_phone2_edit.insert(0, phone.split('-')[1])

    tk.Label(new_tab, text="-").grid(row=2, column=4, padx=0, pady=5)

    entry_phone3_edit = tk.Entry(new_tab, validate="key", validatecommand=(phone_validate, '%P'), width=4)
    entry_phone3_edit.grid(row=2, column=5, padx=0, pady=5)
    entry_phone3_edit.insert(0, phone.split('-')[2])
    
    tk.Label(new_tab, text="이메일:").grid(row=3, column=0, padx=10, pady=5)
    tk.Label(new_tab, text="주소:").grid(row=4, column=0, padx=10, pady=5)

    entry_name_edit = tk.Entry(new_tab)
    entry_name_edit.grid(row=1, column=1)
    entry_name_edit.insert(0, name)

    entry_email_edit = tk.Entry(new_tab)
    entry_email_edit.grid(row=3, column=1)
    entry_email_edit.insert(0, email)

    entry_address_edit = tk.Entry(new_tab)
    entry_address_edit.grid(row=4, column=1)
    entry_address_edit.insert(0, address)

    def save_edits():
        updated_name = entry_name_edit.get()
        updated_phone = f"{entry_phone1_edit.get()}-{entry_phone2_edit.get()}-{entry_phone3_edit.get()}"
        updated_email = entry_email_edit.get()
        updated_address = entry_address_edit.get()

        # Update customer information using ID
        update_customer(customer_id, updated_name, updated_phone, updated_email, updated_address)
        messagebox.showinfo("저장 완료", "저장되었습니다.")
        load_customers()  # Refresh the customer list
        tab_names.pop(name, None)  # Remove old tab reference
        tab_names[updated_name] = new_tab  # Add updated tab reference
        notebook.tab(new_tab, text=f"{updated_name} [x]")  # Update tab name
        notebook.select(tab_all_customers) 

    save_button_edit = tk.Button(new_tab, text="저장", command=save_edits)
    save_button_edit.grid(row=5, column=1, pady=10)

    def delete_customer_info():
        if messagebox.askyesno("삭제 확인", "정말로 삭제하시겠습니까?"):
            delete_customer(customer_id)
            load_customers()
            close_tab(tab_name, new_tab)
            notebook.select(tab_all_customers)  # Switch to the 전체 고객 tab

    delete_button_edit = tk.Button(new_tab, text="삭제", command=delete_customer_info)
    delete_button_edit.grid(row=6, column=1, pady=10)

    notebook.select(new_tab)  # Switch to the new tab

    # Add tab to the tab_names dictionary
    tab_names[tab_name] = new_tab
    print(f"Tab names updated: {tab_names}")  # Debug print

def close_tab(tab_name, tab_frame):
    if tab_name in tab_names:
        notebook.forget(tab_names[tab_name])  # Remove the tab from notebook
        tab_names.pop(tab_name, None)  # Remove tab from the dictionary
        tab_frame.destroy()  # Explicitly destroy the tab frame

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
treeview_customers = ttk.Treeview(tab_all_customers, columns=("ID", "Name", "Phone", "Email", "Address"), show='headings')
treeview_customers.heading("ID", text="ID")
treeview_customers.heading("Name", text="이름")
treeview_customers.heading("Phone", text="전화번호")
treeview_customers.heading("Email", text="이메일")
treeview_customers.heading("Address", text="주소")

treeview_customers.column("ID", width=50, anchor="w")
treeview_customers.column("Name", width=150, anchor="w")
treeview_customers.column("Phone", width=150, anchor="w")
treeview_customers.column("Email", width=150, anchor="w")
treeview_customers.column("Address", width=200, anchor="w")

treeview_customers.pack(padx=10, pady=10, fill="both", expand=True)
treeview_customers.bind("<Double-1>", show_customer_info)

load_customers()

# 두 번째 탭: 고객 추가
tab_add_customer = ttk.Frame(notebook)
notebook.add(tab_add_customer, text="고객 추가")

tk.Label(tab_add_customer, text="이름:").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(tab_add_customer)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(tab_add_customer, text="전화번호:").grid(row=1, column=0, padx=10, pady=5)
phone_validate = root.register(lambda input: input.isdigit() or input == '')  # 숫자만 허용하는 validation 함수
entry_phone1 = tk.Entry(tab_add_customer, validate="key", validatecommand=(phone_validate, '%P'), width=5)
entry_phone1.grid(row=1, column=1, padx=10, pady=5)
entry_phone1.insert(0, "010")
tk.Label(tab_add_customer, text="-").grid(row=1, column=2, padx=0, pady=5)
entry_phone2 = tk.Entry(tab_add_customer, validate="key", validatecommand=(phone_validate, '%P'), width=4)
entry_phone2.grid(row=1, column=3, padx=0, pady=5)
tk.Label(tab_add_customer, text="-").grid(row=1, column=4, padx=0, pady=5)
entry_phone3 = tk.Entry(tab_add_customer, validate="key", validatecommand=(phone_validate, '%P'), width=4)
entry_phone3.grid(row=1, column=5, padx=0, pady=5)

tk.Label(tab_add_customer, text="이메일:").grid(row=2, column=0, padx=10, pady=5)
entry_email = tk.Entry(tab_add_customer)
entry_email.grid(row=2, column=1, padx=10, pady=5)

tk.Label(tab_add_customer, text="주소:").grid(row=3, column=0, padx=10, pady=5)
entry_address = tk.Entry(tab_add_customer)
entry_address.grid(row=3, column=1, padx=10, pady=5)

save_button = tk.Button(tab_add_customer, text="저장", command=save_customer)
save_button.grid(row=4, column=1, padx=10, pady=10)

# 고객 편집 탭 저장을 위한 딕셔너리
tab_names = {}

root.mainloop()

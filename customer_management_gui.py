import tkinter as tk
from tkinter import ttk, messagebox
from sql import add_customer, get_customers, delete_customer, update_customer, close_connection, get_customer_by_id, get_customer_id_by_info

def save_customer():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()
    
    # 고객 추가
    add_customer(name, phone, email, address)
    messagebox.showinfo("저장 완료", "저장되었습니다.")
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    load_customers()

def load_customers(query=""):
    customers = get_customers(query)
    treeview_customers.delete(*treeview_customers.get_children())
    for customer in customers:
        # Ensure the order is (name, phone, email, address)
        treeview_customers.insert('', tk.END, values=(customer[1], customer[2], customer[3], customer[4]))



def delete_selected_customer():
    selected_item = treeview_customers.selection()
    if selected_item:
        customer_values = treeview_customers.item(selected_item)['values']
        name, phone, email, address = customer_values
        customer_id = get_customer_id_by_info(name, phone, email, address)
        if customer_id:
            if messagebox.askyesno("삭제 확인", "선택한 고객을 삭제하시겠습니까?"):
                delete_customer(customer_id)
                load_customers()
        else:
            messagebox.showerror("오류", "고객 정보를 찾을 수 없습니다.")


def show_customer_info(event):
    selected_item = treeview_customers.selection()
    if selected_item:
        customer_values = treeview_customers.item(selected_item)['values']
        if len(customer_values) >= 4:
            # Extract values in the correct order
            name, phone, email, address = customer_values
            # Retrieve the customer ID from the selection (needs correct indexing)
            customer_id = get_customer_id_by_info(name, phone, email, address)
            if customer_id:
                create_customer_tab(customer_id, name, phone, email, address)

def show_customer_info(event):
    selected_item = treeview_customers.selection()
    if selected_item:
        customer_values = treeview_customers.item(selected_item)['values']
        if len(customer_values) >= 4:
            name, phone, email, address = customer_values
            customer_id = get_customer_id_by_info(name, phone, email, address)
            
            if customer_id:
                create_customer_tab(customer_id, name, phone, email, address)
            else:
                messagebox.showerror("오류", "고객 정보를 찾을 수 없습니다.")
        else:
            messagebox.showerror("오류", "올바른 고객 데이터를 선택하세요.")

def search_customers(event=None):
    search_term = entry_search.get()
    load_customers(search_term)

def create_customer_tab(customer_id, name, phone, email, address):
    tab_name = name
    
    # 이미 존재하는 탭인지 확인하고, 있다면 해당 탭으로 이동
    if tab_name in tab_names:
        notebook.select(tab_names[tab_name])
        return

    # 새로운 탭 생성
    new_tab = ttk.Frame(notebook)
    notebook.add(new_tab, text=f"{tab_name} [x]")
    
    # Tab에 이름을 저장해 관리
    tab_names[tab_name] = new_tab

    # Tab 내에 고객 정보를 표시
    tk.Label(new_tab, text="이름:").grid(row=0, column=0, padx=10, pady=5)
    entry_name_edit = tk.Entry(new_tab)
    entry_name_edit.grid(row=0, column=1, padx=10, pady=5)
    entry_name_edit.insert(0, name)

    tk.Label(new_tab, text="전화번호:").grid(row=1, column=0, padx=10, pady=5)
    entry_phone_edit = tk.Entry(new_tab)
    entry_phone_edit.grid(row=1, column=1, padx=10, pady=5)
    entry_phone_edit.insert(0, phone)

    tk.Label(new_tab, text="이메일:").grid(row=2, column=0, padx=10, pady=5)
    entry_email_edit = tk.Entry(new_tab)
    entry_email_edit.grid(row=2, column=1, padx=10, pady=5)
    entry_email_edit.insert(0, email)

    tk.Label(new_tab, text="주소:").grid(row=3, column=0, padx=10, pady=5)
    entry_address_edit = tk.Entry(new_tab)
    entry_address_edit.grid(row=3, column=1, padx=10, pady=5)
    entry_address_edit.insert(0, address)

    # 정보 저장 버튼
    def save_edits():
        updated_name = entry_name_edit.get()
        updated_phone = entry_phone_edit.get()
        updated_email = entry_email_edit.get()
        updated_address = entry_address_edit.get()

        # 고객 정보 업데이트
        update_customer(customer_id, updated_name, updated_phone, updated_email, updated_address)
        messagebox.showinfo("저장 완료", "정보가 저장되었습니다.")
        load_customers()

        # 탭 이름 업데이트
        tab_names.pop(name, None)
        tab_names[updated_name] = new_tab
        notebook.tab(new_tab, text=f"{updated_name} [x]")

    save_button_edit = tk.Button(new_tab, text="저장", command=save_edits)
    save_button_edit.grid(row=4, column=1, pady=10)

    # 정보 삭제 버튼
    def delete_customer_info():
        if messagebox.askyesno("삭제 확인", "정말로 삭제하시겠습니까?"):
            delete_customer(customer_id)
            load_customers()
            close_tab(tab_name, new_tab)

    delete_button_edit = tk.Button(new_tab, text="삭제", command=delete_customer_info)
    delete_button_edit.grid(row=5, column=1, pady=10)

    notebook.select(new_tab)  # 새로운 탭으로 포커스 이동



def close_tab(tab_name, tab_frame):
    tab = tab_names.pop(tab_name, None)
    if tab:
        notebook.forget(tab_frame)
        
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
treeview_customers = ttk.Treeview(tab_all_customers, columns=("Name", "Phone", "Email", "Address"), show='headings')
treeview_customers.heading("Name", text="이름")
treeview_customers.heading("Phone", text="전화번호")
treeview_customers.heading("Email", text="이메일")
treeview_customers.heading("Address", text="주소")

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
entry_phone = tk.Entry(tab_add_customer)
entry_phone.grid(row=1, column=1, padx=10, pady=5)

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
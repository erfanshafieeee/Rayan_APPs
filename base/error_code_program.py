import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from pathlib import Path

def start_error_code_program():
    PASSWORD = "1234"
    
    # پیدا کردن مسیر پوشه Documents کاربر
    documents_path = Path.home() / "Documents/RayanApps"
    if not documents_path.exists():
        documents_path.mkdir(parents=True)  # ایجاد دایرکتوری اگر وجود ندارد

    # گرفتن مسیر فایل JSON در Documents
    json_file_path = os.path.join(documents_path, 'errors.json')

    # بررسی اینکه فایل JSON وجود دارد یا خیر. اگر وجود نداشت، یک فایل جدید خالی ایجاد می‌شود
    def create_empty_json_if_not_exists():
        if not os.path.exists(json_file_path):
            empty_data = {"errors": {}}  # ساختار خالی JSON
            with open(json_file_path, 'w') as file:
                json.dump(empty_data, file, indent=4)

    # تابع برای چک کردن پسورد
    def check_password():
        entered_password = simpledialog.askstring("Password", "Enter the password:", show='*')
        return entered_password == PASSWORD

    # تابع برای خروجی گرفتن از فایل JSON
    def export_json():
        if check_password():
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                try:
                    with open(json_file_path, 'r') as original_file:
                        data = json.load(original_file)
                    with open(file_path, 'w') as export_file:
                        json.dump(data, export_file, indent=4)
                    messagebox.showinfo("Export", "File exported successfully.")
                except Exception as e:
                    messagebox.showerror("Export Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")

    # تابع برای وارد کردن فایل JSON
    def import_json():
        if check_password():
            file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            if file_path:
                try:
                    with open(json_file_path, 'r') as original_file:
                        original_data = json.load(original_file)
                    with open(file_path, 'r') as import_file:
                        new_data = json.load(import_file)
                    
                    # مقایسه و ادغام داده‌ها
                    updated = False
                    for code, details in new_data.get("errors", {}).items():
                        if code not in original_data.get("errors", {}):
                            original_data["errors"][code] = details
                            updated = True
                    
                    if updated:
                        with open(json_file_path, 'w') as original_file:
                            json.dump(original_data, original_file, indent=4)
                        messagebox.showinfo("Import", "New data has been added successfully.")
                    else:
                        messagebox.showinfo("Import", "No new data to add.")
                except Exception as e:
                    messagebox.showerror("Import Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")

    # تابع برای اضافه کردن دستی یک کد خطا
    def add_error_code():
        if check_password():
            code = simpledialog.askstring("Add Error Code", "Enter the State error code:", parent=root)
            
            # اضافه کردن پیشوند '0x' اگر نباشد
            if not code.startswith('0x'):
                code = '0x' + code
                
            summary = simpledialog.askstring("Add Summary", "Enter the summary (in English):", parent=root)
            description = simpledialog.askstring("Add Description", "Enter the description (in English):", parent=root)
            
            try:
                with open(json_file_path, 'r') as file:
                    data = json.load(file)
                
                if code in data.get("errors", {}):
                    messagebox.showerror("Error", "This code already exists.", parent=root)
                else:
                    data["errors"][code] = {
                        "summary": summary,
                        "description": description
                    }
                    with open(json_file_path, 'w') as file:
                        json.dump(data, file, indent=4)
                    messagebox.showinfo("Success", "Error code added successfully.", parent=root)
            except Exception as e:
                messagebox.showerror("Add Error", f"An error occurred: {str(e)}", parent=root)
        else:
            messagebox.showerror("Access Denied", "Incorrect password.", parent=root)

    # تابع برای جستجوی کد خطا در فایل JSON
    def search_error(event=None):
        code = entry_code.get().strip().upper()
        code = code.replace("X","x")
        # اضافه کردن پیشوند '0x' اگر نباشد
        if not (code.startswith("0x")):
            code = "0x" + code
        
        # خواندن فایل JSON
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                errors = data.get("errors", {})
                error_info = errors.get(code)
                
                # اگر کد مستقیم پیدا نشد، بررسی بازه‌ها
                if not error_info:
                    for range_str, details in errors.items():
                        if '-' in range_str and code_in_range(code, range_str):
                            error_info = details
                            break
                
                if error_info:
                    summary = error_info['summary']
                    description = error_info['description']
                    label_summary_value.config(text=summary)
                    label_description_value.config(text=description)
                else:
                    messagebox.showerror("Error", "Error code not found in database.")
        except FileNotFoundError:
            messagebox.showerror("Error", "JSON file not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error reading JSON file.")

    # تابعی برای بررسی اینکه کد در بازه مشخص شده است یا خیر
    def code_in_range(code, range_str):
        start_str, end_str = range_str.split('-')
        start_code = int(start_str, 16)
        end_code = int(end_str, 16)
        code = int(code, 16)
        return start_code <= code <= end_code

    def quit_app():
        root.withdraw()
        root.quit()

    # ایجاد فایل JSON خالی در صورت عدم وجود
    create_empty_json_if_not_exists()

    # ایجاد پنجره اصلی
    root = tk.Tk()
    root.title("State Error Code Finder")
    # تنظیمات اندازه و رنگ پنجره
    root.geometry("1200x600")
    root.configure(bg='#F0A07C')
    # لیبل و ورودی برای کد خطا
    label_code = tk.Label(root, text="Enter your state error code:", bg='#F0A07C', font=('Helvetica', 15, 'bold') , fg='white')
    label_code.pack(pady=5)
    entry_code = tk.Entry(root)
    entry_code.pack(pady=5)
    # دکمه جستجو با رنگ متمایز
    search_button = tk.Button(root, text="Search", command=search_error, bg='blue', fg='white', font=('Helvetica', 15, 'bold'))
    search_button.pack(pady=10)
    # متصل کردن دکمه Enter به تابع جستجو
    root.bind('<Return>', search_error)
    # نمایش خلاصه و شرح خطا
    label_summary = tk.Label(root, text="Summary:", bg='#F0A07C', font=('Helvetica', 15, 'bold'),fg='white')
    label_summary.pack(pady=5)
    label_summary_value = tk.Label(root, text="", fg="blue", bg='#F0A07C', font=('Helvetica', 15, 'bold'), wraplength=1200, justify='left')
    label_summary_value.pack(pady=5)
    label_description = tk.Label(root, text="Description:", bg='#F0A07C', font=('Helvetica', 15, 'bold'),fg='white')
    label_description.pack(pady=5)
    label_description_value = tk.Label(root, text="", fg="green", bg='#F0A07C', font=('Helvetica', 15, 'bold'), wraplength=1200, justify='left')
    label_description_value.pack(pady=5)
    # دکمه‌های اضافی برای وارد کردن، خروجی گرفتن و اضافه کردن دستی کد خطا
    button_frame = tk.Frame(root, bg='#F0A07C')
    button_frame.pack(pady=20)
    export_button = tk.Button(button_frame, text="Export JSON", command=export_json, bg='#4A274F', fg='white', font=('Helvetica', 15, 'bold'))
    export_button.pack(side='left', padx=10)
    import_button = tk.Button(button_frame, text="Import JSON", command=import_json, bg='#4A274F', fg='white',font=('Helvetica', 15, 'bold'))
    import_button.pack(side='left', padx=10)
    add_button = tk.Button(button_frame, text="Add Error Code", command=add_error_code, bg='#4A274F', fg='white', font=('Helvetica', 15, 'bold'))
    add_button.pack(side='left', padx=10)
    btn_exit = tk.Button(button_frame, text="Exit", command=quit_app, bg='#4A274F', fg='white', font=('Helvetica', 15, 'bold'))
    btn_exit.pack(side='left', padx=10)
    # اجرای برنامه
    root.mainloop()


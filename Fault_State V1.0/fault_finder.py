import json
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, font

PASSWORD = "1234"

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
                with open('errors.json', 'r') as original_file:
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
                with open('errors.json', 'r') as original_file:
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
                    with open('errors.json', 'w') as original_file:
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
        code = simpledialog.askstring("Add Error Code", "Enter the error code:")
        
        # اضافه کردن پیشوند '0x' اگر نباشد
        if not code.startswith('0x'):
            code = '0x' + code
        
        summary = simpledialog.askstring("Add Summary", "Enter the summary (in English):")
        description = simpledialog.askstring("Add Description", "Enter the description (in English):")
        
        try:
            with open('errors.json', 'r') as file:
                data = json.load(file)
            
            if code in data.get("errors", {}):
                messagebox.showerror("Error", "This code already exists.")
            else:
                data["errors"][code.upper()] = {
                    "summary": summary,
                    "description": description
                }
                with open('errors.json', 'w') as file:
                    json.dump(data, file, indent=4)
                messagebox.showinfo("Success", "Error code added successfully.")
        except Exception as e:
            messagebox.showerror("Add Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showerror("Access Denied", "Incorrect password.")

# تابع برای بررسی اینکه یک کد در یک بازه قرار دارد یا نه
def code_in_range(code, range_str):
    start, end = range_str.split('-')
    start = int(start, 16)
    end = int(end, 16)
    code = int(code, 16)
    return start <= code <= end

# تابع برای جستجوی کد خطا در فایل JSON
def search_error(event=None):
    code = entry_code.get().strip().upper()
    
    # اضافه کردن پیشوند '0x' اگر نباشد
    if not code.startswith('0x'):
        code = '0x' + code
    
    # خواندن فایل JSON
    try:
        with open('errors.json', 'r') as file:
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

# ایجاد پنجره اصلی
root = tk.Tk()
root.title("Error Code Lookup")

# تنظیمات اندازه و رنگ پنجره
root.geometry("1200x600")
root.configure(bg='orange')

# فونت بولد
bold_font = font.Font(weight='bold')

# لیبل و ورودی برای کد خطا
label_code = tk.Label(root, text="Enter your error code:", bg='orange', font=bold_font)
label_code.pack(pady=5)
entry_code = tk.Entry(root)
entry_code.pack(pady=5)

# دکمه جستجو با رنگ متمایز
search_button = tk.Button(root, text="Search", command=search_error, bg='blue', fg='white', font=bold_font)
search_button.pack(pady=10)

# متصل کردن دکمه Enter به تابع جستجو
root.bind('<Return>', search_error)

# نمایش خلاصه و شرح خطا
label_summary = tk.Label(root, text="Summary:", bg='orange', font=bold_font)
label_summary.pack(pady=5)
label_summary_value = tk.Label(root, text="", fg="blue", bg='orange', font=bold_font, wraplength=1200, justify='left')
label_summary_value.pack(pady=5)

label_description = tk.Label(root, text="Description:", bg='orange', font=bold_font)
label_description.pack(pady=5)
label_description_value = tk.Label(root, text="", fg="green", bg='orange', font=bold_font, wraplength=1200, justify='left')
label_description_value.pack(pady=5)

# دکمه‌های اضافی برای وارد کردن، خروجی گرفتن و اضافه کردن دستی کد خطا
button_frame = tk.Frame(root, bg='orange')
button_frame.pack(pady=20)

export_button = tk.Button(button_frame, text="Export JSON", command=export_json, bg='purple', fg='white', font=bold_font)
export_button.pack(side='left', padx=10)

import_button = tk.Button(button_frame, text="Import JSON", command=import_json, bg='purple', fg='white', font=bold_font)
import_button.pack(side='left', padx=10)

add_button = tk.Button(button_frame, text="Add Error Code", command=add_error_code, bg='purple', fg='white', font=bold_font)
add_button.pack(side='left', padx=10)

# اجرای برنامه
root.mainloop()
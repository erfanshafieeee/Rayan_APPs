import tkinter as tk
from tkinter import messagebox

def calculate_diag_ids(event=None):
    try:
        ecu_id = int(entry_ecu_id.get(), 16)
        diag_id_pos = []
        diag_id_min = []
        digit = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x100, 0x120, 0x200]

        for i in digit:
            x = ecu_id + i
            diag_id_pos.append(hex(x))

        for j in digit:
            y = ecu_id - j
            diag_id_min.append(hex(y))

        # ایجاد خروجی با فاصله بیشتر بین اعداد
        output_pos = f"diag_id maybe:\n{' _ '.join(diag_id_pos)}\n\n"  # فاصله اضافی بعد از لیست
        output_or = "\n\nOR\n\n"  # فاصله اضافی قبل و بعد از "OR"
        output_min = f"diag_id maybe:\n{' _ '.join(diag_id_min)}"

        # پاک کردن متن قبلی
        result_text.delete(1.0, tk.END)

        # درج متن و اعمال استایل
        result_text.insert(tk.END, output_pos, 'green_text')
        result_text.insert(tk.END, output_or, 'black_text')
        result_text.insert(tk.END, output_min, 'red_text')
    
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid hexadecimal number.")

# ایجاد پنجره اصلی
root = tk.Tk()
root.title("Diag_ID_CAN_2A Calculator")

# تنظیم رنگ پس‌زمینه پنجره
root.configure(bg='lightblue')

# برچسب ورودی ECU ID
label_ecu_id = tk.Label(root, text="Enter ECU ID (hex):", bg='lightblue', fg='red', font=('Helvetica', 14))
label_ecu_id.pack(pady=10)

# ورودی ECU ID
entry_ecu_id = tk.Entry(root, font=('Helvetica', 14))
entry_ecu_id.pack(pady=10)

# دکمه محاسبه
btn_calculate = tk.Button(root, text="Calculate", command=calculate_diag_ids, bg='red', fg='white', font=('Helvetica', 14))
btn_calculate.pack(pady=10)

# نمایش نتیجه
result_text = tk.Text(root, height=10, width=125, wrap=tk.WORD, font=('Helvetica', 12), bg='lightblue', fg='black', borderwidth=2, relief='sunken')
result_text.pack(pady=10)

# تنظیم تگ‌ها برای رنگ‌آمیزی
result_text.tag_configure('green_text', foreground='green')
result_text.tag_configure('red_text', foreground='red')
result_text.tag_configure('black_text', foreground='black')

# تنظیم رویداد کلید Enter برای ورودی ECU ID
entry_ecu_id.bind('<Return>', calculate_diag_ids)

# شروع حلقه رویداد GUI
root.mainloop()

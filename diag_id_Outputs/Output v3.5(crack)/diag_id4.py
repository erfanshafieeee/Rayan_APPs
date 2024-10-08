import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json
import os

# دریافت مسیر دایرکتوری فایل اجرایی
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# تعریف مسیر کامل فایل JSON
POPULARITY_FILE = os.path.join(BASE_DIR, 'popularity_data.json')

# Define a key for XOR encryption/decryption
KEY = 'G-eXJZRWOUkoaUhOru1QGylopzzoQ1RX2YIwoFW8aDI='  # This should be a string of the same length as the data or use a fixed length key

def xor_encrypt_decrypt(data, key):
    """Encrypt or decrypt data using XOR."""
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def encrypt_file(file_path):
    """Encrypt the contents of a file."""
    with open(file_path, 'r') as file:
        data = file.read()
    encrypted_data = xor_encrypt_decrypt(data, KEY)
    with open(file_path, 'w') as file:
        file.write(encrypted_data)

def decrypt_file(file_path):
    """Decrypt the contents of a file."""
    with open(file_path, 'r') as file:
        encrypted_data = file.read()
    decrypted_data = xor_encrypt_decrypt(encrypted_data, KEY)
    return decrypted_data

# Load popularity data from file
def load_popularity_data():
    if os.path.exists(POPULARITY_FILE):
        decrypted_data = decrypt_file(POPULARITY_FILE)
        return json.loads(decrypted_data)
    return {}

# Save popularity data to file
def save_popularity_data(data):
    encrypted_data = json.dumps(data)
    with open(POPULARITY_FILE, 'w') as file:
        file.write(xor_encrypt_decrypt(encrypted_data, KEY))

# Update popularity count based on ECU_ID
def update_popularity(ecu_id, diag_id):
    data = load_popularity_data()
    if ecu_id not in data:
        data[ecu_id] = {}
    data[ecu_id][diag_id] = data[ecu_id].get(diag_id, 0) + 1
    save_popularity_data(data)

def calculate_diag_ids(event=None):
    try:
        ecu_id = entry_ecu_id.get().strip().upper()
        # Check if the input starts with '0x'
        if not ecu_id.startswith("0X"):
            ecu_id = "0X" + ecu_id  # Add '0x' prefix if missing

        ecu_id_int = int(ecu_id, 16)
        
        diag_id_pos = []
        diag_id_min = []
        digit = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x100, 0x120, 0x200]

        for i in digit:
            x = ecu_id_int + i
            diag_id_pos.append(hex(x).upper())

        for j in digit:
            y = ecu_id_int - j
            diag_id_min.append(hex(y).upper())

        # Load popularity data
        popularity_data = load_popularity_data()

        # Combine IDs and sort by popularity for the specific ECU_ID
        all_ids = diag_id_pos + diag_id_min
        if ecu_id in popularity_data:
            all_ids.sort(key=lambda id: popularity_data[ecu_id].get(id, 0), reverse=True)

        # Clear previous widgets
        result_text.delete(1.0, tk.END)
        listbox.delete(0, tk.END)

        # Display the top 3 popular diagnostic IDs
        top_3_ids = all_ids[:3]
        output_most_popular = "Top 3 Most Popular diag_ids for this ECU_ID:\n"
        output_most_popular += "\n".join([f"{i}" for i in top_3_ids]) + "\n\n" if top_3_ids else ""
        result_text.insert(tk.END, output_most_popular, 'blue_text')

        # Add diagnostic IDs to the listbox
        for diag_id in all_ids:
            listbox.insert(tk.END, diag_id)

        # Add diagnostic ID lists below
        output_pos = f"diag_id maybe:\n{' _ '.join(diag_id_pos)}\n\n"
        output_or = "\nOR\n"
        output_min = f"diag_id maybe:\n\n{' _ '.join(diag_id_min)}"

        result_text.insert(tk.END, output_pos, 'green_text')
        result_text.insert(tk.END, output_or, 'black_text')
        result_text.insert(tk.END, output_min, 'red_text')

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid hexadecimal number.")

def submit_selection():
    try:
        ecu_id = entry_ecu_id.get().strip().upper()
        # Check if the input starts with '0x'
        if not ecu_id.startswith("0X"):
            ecu_id = "0X" + ecu_id  # Add '0x' prefix if missing
            
        selected_index = listbox.curselection()
        if selected_index:
            selected_id = listbox.get(selected_index)
            update_popularity(ecu_id, selected_id)
            messagebox.showinfo("Submission Successful", f"Submitted ID: {selected_id}")
            calculate_diag_ids()  # Refresh to show updated correct ID
        else:
            messagebox.showwarning("No Selection", "Please select an ID from the list.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_else_diag_id():
    ecu_id = entry_ecu_id.get().strip().upper()
    if not ecu_id.startswith("0X"):
        ecu_id = "0X" + ecu_id  # Add '0x' prefix if missing

    else_diag_id = simpledialog.askstring("Else diag_id", "Please enter an additional diag_id (hex):").strip().upper()
    if else_diag_id:
        if not else_diag_id.startswith("0X"):
            else_diag_id = "0X" + else_diag_id

        update_popularity(ecu_id, else_diag_id)
        messagebox.showinfo("Else diag_id Added", f"Added diag_id: {else_diag_id}")
        calculate_diag_ids()  # Refresh to show updated correct ID

def reset():
    # Clear the input field and result area
    entry_ecu_id.delete(0, tk.END)
    result_text.delete(1.0, tk.END)
    listbox.delete(0, tk.END)

    # Clear the popularity data file
    if os.path.exists(POPULARITY_FILE):
        os.remove(POPULARITY_FILE)

def export_json():
    def check_password():
        password = simpledialog.askstring("Password", "Enter password to export JSON file:")
        if password == "erfan5183":
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                encrypt_file(POPULARITY_FILE)  # Encrypt before exporting
                with open(POPULARITY_FILE, 'r') as file:
                    data = file.read()
                with open(file_path, 'w') as file:
                    file.write(data)
                messagebox.showinfo("Export Successful", "File exported successfully.")
                encrypt_file(POPULARITY_FILE)  # Re-encrypt after exporting
        else:
            messagebox.showerror("Error", "Incorrect password.")

    check_password()

def import_json():
    def check_password():
        password = simpledialog.askstring("Password", "Enter password to import JSON file:")
        if password == "erfan5183":
            file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            if file_path:
                with open(file_path, 'r') as file:
                    imported_data = file.read()
                # Decrypt the imported data
                decrypted_data = xor_encrypt_decrypt(imported_data, KEY)
                new_data = json.loads(decrypted_data)

                existing_data = load_popularity_data()

                # Merge new data with existing data
                for ecu_id, diag_ids in new_data.items():
                    if ecu_id not in existing_data:
                        existing_data[ecu_id] = {}
                    for diag_id, count in diag_ids.items():
                        existing_data[ecu_id][diag_id] = existing_data[ecu_id].get(diag_id, 0) + count

                save_popularity_data(existing_data)
                messagebox.showinfo("Import Successful", "Data imported and merged successfully.")
        else:
            messagebox.showerror("Error", "Incorrect password.")

    check_password()

root = tk.Tk()
root.title("Diag_ID_CAN_2A Calculator")
root.configure(bg='lightblue')

# Frame for ID input and buttons
frame_main = tk.Frame(root, bg='lightblue')
frame_main.pack(pady=10, padx=10, fill=tk.X)

label_ecu_id = tk.Label(frame_main, text="Enter ECU ID (hex):", bg='lightblue', fg='red', font=('Helvetica', 14, 'bold'))
label_ecu_id.pack(pady=10, side=tk.LEFT)

entry_ecu_id = tk.Entry(frame_main, font=('Helvetica', 14, 'bold'))
entry_ecu_id.pack(pady=10, side=tk.LEFT)

frame_buttons = tk.Frame(frame_main, bg='lightblue')
frame_buttons.pack(pady=10, side=tk.RIGHT, anchor=tk.CENTER)

btn_calculate = tk.Button(frame_buttons, text="Calculate", command=calculate_diag_ids, bg='red', fg='white', font=('Helvetica', 14, 'bold'))
btn_calculate.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

btn_export = tk.Button(frame_buttons, text="Export JSON", command=export_json, bg='blue', fg='white', font=('Helvetica', 10, 'bold'))
btn_export.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

btn_import = tk.Button(frame_buttons, text="Import JSON", command=import_json, bg='green', fg='white', font=('Helvetica', 10, 'bold'))
btn_import.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

# Create a larger Text widget for displaying the results
result_text = tk.Text(root, height=14, width=80, wrap=tk.WORD, font=('Helvetica', 12, 'bold'), bg='lightblue', fg='black', borderwidth=2, relief='sunken')
result_text.pack(pady=10)

# Frame for Listbox and Submit Button
frame_listbox = tk.Frame(root, bg='lightblue')
frame_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

# Label above Listbox
label_listbox = tk.Label(frame_listbox, text="Which one is correct?", bg='lightblue', fg='blue', font=('Helvetica', 14, 'bold'))
label_listbox.pack(pady=10)

# Create a larger Listbox widget for selecting diagnostic IDs
listbox = tk.Listbox(frame_listbox, font=('Helvetica', 12, 'bold'), selectmode=tk.SINGLE, bg='lightblue', fg='black')
listbox.pack(pady=10, fill=tk.BOTH, expand=True)

# Frame for Submit and Else buttons
frame_buttons = tk.Frame(frame_listbox, bg='lightblue')
frame_buttons.pack(pady=10)

btn_submit = tk.Button(frame_buttons, text="Submit", command=submit_selection, bg='green', fg='white', font=('Helvetica', 14, 'bold'))
btn_submit.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

btn_else = tk.Button(frame_buttons, text="Else", command=add_else_diag_id, bg='orange', fg='white', font=('Helvetica', 14, 'bold'))
btn_else.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

# Configure tags for text colors
result_text.tag_configure('blue_text', foreground='blue')
result_text.tag_configure('green_text', foreground='green')
result_text.tag_configure('red_text', foreground='red')
result_text.tag_configure('black_text', foreground='black')

# Bind Enter key to calculate_diag_ids
entry_ecu_id.bind('<Return>', calculate_diag_ids)

root.mainloop()
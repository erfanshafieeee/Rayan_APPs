import tkinter as tk
from tkinter import messagebox
import json
import os


# دریافت مسیر دایرکتوری فایل اجرایی
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# تعریف مسیر کامل فایل JSON
POPULARITY_FILE = os.path.join(BASE_DIR, 'popularity_data.json')

# # File to store popularity data
# POPULARITY_FILE = 'popularity_data.json'

# Load popularity data from file
def load_popularity_data():
    if os.path.exists(POPULARITY_FILE):
        with open(POPULARITY_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save popularity data to file
def save_popularity_data(data):
    with open(POPULARITY_FILE, 'w') as file:
        json.dump(data, file)

# Update popularity count
def update_popularity(diag_id):
    data = load_popularity_data()
    data[diag_id] = data.get(diag_id, 0) + 1
    save_popularity_data(data)

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

        # Load popularity data
        popularity_data = load_popularity_data()

        # Combine IDs and sort by popularity
        all_ids = diag_id_pos + diag_id_min
        all_ids.sort(key=lambda id: popularity_data.get(id, 0), reverse=True)

        # Clear previous widgets
        result_text.delete(1.0, tk.END)
        listbox.delete(0, tk.END)

        # Display the top 3 popular diagnostic IDs
        top_3_ids = all_ids[:3]
        output_most_popular = "Top 3 Most Popular diag_ids:\n"
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
        selected_index = listbox.curselection()
        if selected_index:
            selected_id = listbox.get(selected_index)
            update_popularity(selected_id)
            messagebox.showinfo("Submission Successful", f"Submitted ID: {selected_id}")
            calculate_diag_ids()  # Refresh to show updated correct ID
        else:
            messagebox.showwarning("No Selection", "Please select an ID from the list.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def reset():
    # Clear the input field and result area
    entry_ecu_id.delete(0, tk.END)
    result_text.delete(1.0, tk.END)
    listbox.delete(0, tk.END)

    # Clear the popularity data file
    if os.path.exists(POPULARITY_FILE):
        os.remove(POPULARITY_FILE)

root = tk.Tk()
root.title("Diag_ID_CAN_2A Calculator")
root.configure(bg='lightblue')

# Frame for ID input and buttons
frame_main = tk.Frame(root, bg='lightblue')
frame_main.pack(pady=10, padx=10, fill=tk.X)

label_ecu_id = tk.Label(frame_main, text="Enter ECU ID (hex):", bg='lightblue', fg='red', font=('Helvetica', 14))
label_ecu_id.pack(pady=10)

entry_ecu_id = tk.Entry(frame_main, font=('Helvetica', 14))
entry_ecu_id.pack(pady=10)

btn_calculate = tk.Button(frame_main, text="Calculate", command=calculate_diag_ids, bg='red', fg='white', font=('Helvetica', 14))
btn_calculate.pack(pady=10)

# Create a larger Text widget for displaying the results
result_text = tk.Text(root, height=14, width=80, wrap=tk.WORD, font=('Helvetica', 12), bg='lightblue', fg='black', borderwidth=2, relief='sunken')
result_text.pack(pady=10)

# Frame for Listbox and Submit Button
frame_listbox = tk.Frame(root, bg='lightblue')
frame_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

# Label above Listbox
label_listbox = tk.Label(frame_listbox, text="Which one is correct?", bg='lightblue', fg='blue', font=('Helvetica', 14))
label_listbox.pack(pady=10)

# Create a larger Listbox widget for selecting diagnostic IDs
listbox = tk.Listbox(frame_listbox, font=('Helvetica', 12), selectmode=tk.SINGLE, bg='lightblue', fg='black')
listbox.pack(pady=10, fill=tk.BOTH, expand=True)

btn_submit = tk.Button(frame_listbox, text="Submit", command=submit_selection, bg='green', fg='white', font=('Helvetica', 14))
btn_submit.pack(pady=10)

# Configure tags for text colors
result_text.tag_configure('blue_text', foreground='blue')
result_text.tag_configure('green_text', foreground='green')
result_text.tag_configure('red_text', foreground='red')
result_text.tag_configure('black_text', foreground='black')

# Bind Enter key to calculate_diag_ids
entry_ecu_id.bind('<Return>', calculate_diag_ids)

root.mainloop()

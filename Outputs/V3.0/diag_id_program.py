import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json
import os
from pathlib import Path

def start_diag_id_program():
    # دریافت مسیر دایرکتوری فایل اجرایی در پوشه Documents
    def get_database_path():
        documents_path = Path.home() / "Documents/RayanApps"
        if not documents_path.exists():
            documents_path.mkdir(parents=True)  # ایجاد دایرکتوری اگر وجود ندارد

        return os.path.join(documents_path, 'popularity_data.json')

    POPULARITY_FILE = get_database_path()

    # Load popularity data from file
    def load_popularity_data():
        if os.path.exists(POPULARITY_FILE):
            with open(POPULARITY_FILE, 'r') as file:
                return json.load(file)
        return {}

    # Save popularity data to file
    def save_popularity_data(data):
        with open(POPULARITY_FILE, 'w') as file:
            json.dump(data, file, indent=4)

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
            digit = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x30, 0x40, 0x60, 0x80, 0x100, 0x120, 0x200,
                     0x0A, 0X0B, 0X0C, 0X0D, 0X0E, 0X0F]

            for i in digit:
                x = ecu_id_int + i
                diag_id_pos.append(hex(x).upper())

            for j in digit:
                y = ecu_id_int - j
                diag_id_min.append(hex(y).upper())

            # Load popularity data
            popularity_data = load_popularity_data()

            # Extract popular IDs for this ECU_ID
            popular_ids = []
            if ecu_id in popularity_data:
                popular_ids = [diag_id for diag_id, count in sorted(popularity_data[ecu_id].items(), key=lambda item: item[1], reverse=True)]
            
            # Combine IDs and sort by popularity for the specific ECU_ID
            all_ids = diag_id_pos + diag_id_min
            all_ids = list(set(all_ids))  # Remove duplicates
            
            # Ensure the most popular IDs are considered first
            sorted_ids = list(set(popular_ids + all_ids))
            sorted_ids.sort(key=lambda id: popularity_data.get(ecu_id, {}).get(id, 0), reverse=True)

            # Determine how many IDs to show
            num_top_ids = min(len(popular_ids), 5)
            top_ids = sorted_ids[:num_top_ids]

            # Clear previous widgets
            result_text.delete(1.0, tk.END)
            listbox.delete(0, tk.END)

            # Display the top IDs
            if top_ids:
                output_most_popular = "Suggestions:\n"
                output_most_popular += "\n".join([f"{i}" for i in top_ids]) + "\n\n" if top_ids else ""
                result_text.insert(tk.END, output_most_popular, 'blue_text')
            else:
                result_text.insert(tk.END, "nothing\n\n", 'blue_text')

            # Add diagnostic IDs to the listbox in the order they were generated
            for diag_id in sorted_ids:
                listbox.insert(tk.END, diag_id)

            # Add diagnostic ID lists below
            output_pos = f"diag_id maybe:\n{' _ '.join(diag_id_pos)}\n"
            output_or = "\nOR\n\n"
            output_min = f"diag_id maybe:\n{' _ '.join(diag_id_min)}"

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
                    with open(POPULARITY_FILE, 'r') as file:
                        data = file.read()
                    with open(file_path, 'w') as file:
                        file.write(data)
                    messagebox.showinfo("Export Successful", "File exported successfully.")
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
                        new_data = json.load(file)

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

    def quit_app():
        root.withdraw()
        root.quit()

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

    btn_else_diag_id = tk.Button(frame_buttons, text="Add Else diag_id", command=add_else_diag_id, bg='purple', fg='white', font=('Helvetica', 10, 'bold'))
    btn_else_diag_id.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

    btn_submit = tk.Button(frame_buttons, text="Submit Selection", command=submit_selection, bg='orange', fg='white', font=('Helvetica', 10, 'bold'))
    btn_submit.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

    btn_exit = tk.Button(frame_buttons, text="Exit", command=quit_app, bg='black', fg='white', font=('Helvetica', 10, 'bold'))
    btn_exit.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

    # Create a larger Text widget for displaying the results
    frame_result = tk.Frame(root, bg='lightblue')
    frame_result.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    result_text = tk.Text(frame_result, height=14, width=150, wrap=tk.WORD, font=('Helvetica', 12, 'bold'), bg='lightblue', fg='black', borderwidth=2, relief='sunken')
    result_text.pack(pady=10, fill=tk.BOTH, expand=True)

    # Frame for Listbox and Submit Button
    frame_listbox = tk.Frame(root, bg='lightblue')
    frame_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    # Label above Listbox
    label_listbox = tk.Label(frame_listbox, text="Which one is correct?", bg='lightblue', fg='blue', font=('Helvetica', 14, 'bold'))
    label_listbox.pack(pady=10)

    # Create a larger Listbox widget for selecting diagnostic IDs
    listbox = tk.Listbox(frame_listbox, font=('Helvetica', 12, 'bold'), selectmode=tk.SINGLE, bg='lightblue', fg='black', width=150)
    listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    # Configure tags for text colors
    result_text.tag_configure('blue_text', foreground='blue')
    result_text.tag_configure('green_text', foreground='green')
    result_text.tag_configure('red_text', foreground='red')
    result_text.tag_configure('black_text', foreground='black')

    # Bind Enter key to calculate_diag_ids
    entry_ecu_id.bind('<Return>', calculate_diag_ids)

    root.mainloop()

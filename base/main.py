import tkinter as tk
from diag_id_program import start_diag_id_program
from error_code_program import start_error_code_program


def open_diag_id_program():
    root.withdraw()  # Hide the main window
    start_diag_id_program()
    root.deiconify()  # Show the main window after closing the second window

def open_error_code_program():
    root.withdraw()  # Hide the main window
    start_error_code_program()
    root.deiconify()  # Show the main window after closing the second window


root = tk.Tk()
root.title("Main Menu")
root.geometry("500x500")
root.configure(bg='#243665')





label = tk.Label(root, text="Please select your program:", font=('Helvetica', 14, 'bold'), bg='#243665',fg='#8BD8BD')
label.pack(pady=20)
label = tk.Label(root, text="By Erfan Shafiee", font=('Helvetica', 10, 'bold'), bg='#243665',fg='#8BD8BD')
label.pack(pady=20 , side ="bottom")

btn_diag_id = tk.Button(root, text="آیدی یاب", command=open_diag_id_program, bg='#8BD8BD', fg='black', font=('Helvetica', 12, 'bold'))
btn_diag_id.pack(pady=10, fill=tk.X)

btn_error_code = tk.Button(root, text="خطا یاب", command=open_error_code_program, bg='#8BD8BD', fg='black', font=('Helvetica', 12, 'bold'))
btn_error_code.pack(pady=10, fill=tk.X)

btn_exit = tk.Button(root, text="Exit", command=root.quit, bg='#8BD8BD', fg='black', font=('Helvetica', 10, 'bold'))
btn_exit.pack(pady=10, fill=tk.X)
root.mainloop()

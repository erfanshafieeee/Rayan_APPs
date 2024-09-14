import tkinter as tk
from tkinter import messagebox

# Function to convert hex number to 8-bit binary array
def to_binary_array(hex_num):
    return [int(x) for x in format(hex_num, '08b')]

# Function to calculate mask by comparing new state with all previous states
def calculate_mask(new_state, previous_states):
    mask = [0] * 8
    for prev_state in previous_states:
        for i in range(8):
            if new_state[i] != prev_state[i]:
                mask[i] = 1
    return mask

# Function to add a new state
def add_state(event=None):  # Add 'event=None' to handle both button click and Enter key press
    try:
        state_name = state_entry.get()
        start_value = int(start_entry.get(), 16)  # Convert hex input to decimal
        
        # Convert the starting value to binary
        binary_start_value = to_binary_array(start_value)
        
        if state_name in states:
            messagebox.showerror("Error", "State already exists!")
            return
        
        # Calculate mask only if there are previous states
        if states:
            # Compare with all previous states and calculate the mask
            previous_states = [state['binary'] for state in states.values()]
            mask = calculate_mask(binary_start_value, previous_states)
            mask_value = int("".join(map(str, mask)), 2)  # Convert mask array to an integer
            mask_label.config(text=f"Mask: 0x{mask_value:02X}")
        else:
            mask_label.config(text="Mask: N/A (First state)")
            mask_value = 0xFF  # Assume full mask for first state
        
        # Calculate value (start_value AND mask_value)
        calculated_value = start_value & mask_value
        value_display = f"{calculated_value}"
        
        # Add the new state along with its value
        states[state_name] = {'binary': binary_start_value, 'value': value_display}
        states_listbox.insert(tk.END, f"{state_name}: {binary_start_value}, Value: {value_display}")
        
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid hexadecimal number.")

# Function to reset all data
def reset_data(event=None):  # Add 'event=None' to handle both button click and ESC key press
    states.clear()  # Clear the dictionary
    states_listbox.delete(0, tk.END)  # Clear the Listbox
    mask_label.config(text="Mask:")  # Reset the mask label

# GUI setup
root = tk.Tk()
root.title("Mask Calculator")
root.geometry("800x800")  # Enlarging the window size
root.configure(bg='#1a1a1d')

# State entry
state_label = tk.Label(root, text="Enter state name:", font=("Arial", 14), bg='#1a1a1d', fg='#c3073f')
state_label.pack(pady=10)
state_entry = tk.Entry(root, font=("Arial", 14), width=20, bg='#4e4e50', fg='#ffffff')
state_entry.pack(pady=5)

# Hexadecimal start entry
start_label = tk.Label(root, text="Enter start hex number:", font=("Arial", 14), bg='#1a1a1d', fg='#c3073f')
start_label.pack(pady=10)
start_entry = tk.Entry(root, font=("Arial", 14), width=20, bg='#4e4e50', fg='#ffffff')
start_entry.pack(pady=5)

# Add state button
add_button = tk.Button(root, text="Add State", font=("Arial", 14), command=add_state, bg="#c3073f", fg="#ffffff")
add_button.pack(pady=10)

# Bind Enter key to add_state function
root.bind('<Return>', add_state)

# Display mask
mask_label = tk.Label(root, text="Mask:", font=("Arial", 14), bg='#1a1a1d', fg='#c3073f')
mask_label.pack(pady=10)

# Listbox for showing states
states_listbox = tk.Listbox(root, font=("Arial", 12), width=50, height=12, bg='#4e4e50', fg='#c3073f')
states_listbox.pack(pady=10)

# Reset button
reset_button = tk.Button(root, text="Reset", font=("Arial", 14), command=reset_data, bg="#c3073f", fg="#ffffff")
reset_button.pack(pady=10)

# Bind ESC key to reset_data function
root.bind('<Escape>', reset_data)

# Dictionary to store states
states = {}

# Run the GUI
root.mainloop()

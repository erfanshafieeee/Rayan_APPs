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
def add_state():
    try:
        state_name = state_entry.get()
        state_value = int(index_entry.get(), 16)  # Convert hex input to decimal
        binary_state = to_binary_array(state_value)
        
        if state_name in states:
            messagebox.showerror("Error", "State already exists!")
            return
        
        if states:
            # Compare with all previous states and calculate the mask
            previous_states = list(states.values())
            mask = calculate_mask(binary_state, previous_states)
            mask_value = int("".join(map(str, mask)), 2)  # Convert mask array to an integer
            mask_label.config(text=f"Mask: 0x{mask_value:02X}")
        else:
            mask_label.config(text="Mask: N/A (First state)")
        
        # Add the new state
        states[state_name] = binary_state
        states_listbox.insert(tk.END, f"{state_name}: {binary_state}")
        
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid hexadecimal number.")

# GUI setup
root = tk.Tk()
root.title("State and Mask Calculator")
root.geometry("400x400")  # Enlarging the window size

# State entry
state_label = tk.Label(root, text="Enter state name:", font=("Arial", 14))
state_label.pack(pady=10)
state_entry = tk.Entry(root, font=("Arial", 14), width=20)
state_entry.pack(pady=5)

# Hexadecimal entry
index_label = tk.Label(root, text="Enter hex number (e.g., 0xFF):", font=("Arial", 14))
index_label.pack(pady=10)
index_entry = tk.Entry(root, font=("Arial", 14), width=20)
index_entry.pack(pady=5)

# Add state button
add_button = tk.Button(root, text="Add State", font=("Arial", 14), command=add_state)
add_button.pack(pady=10)

# Display mask
mask_label = tk.Label(root, text="Mask: N/A", font=("Arial", 14))
mask_label.pack(pady=10)

# Listbox for showing states
states_listbox = tk.Listbox(root, font=("Arial", 12), width=30, height=8)
states_listbox.pack(pady=10)

# Dictionary to store states
states = {}

# Run the GUI
root.mainloop()

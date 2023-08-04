import tkinter as tk
from tkinter import ttk

# Define the periods as a dictionary with lists
periods = {
    "p0": ["2023-06-21", "2023-08-03"],
    "p2": ["2023-08-21", "2023-09-03"],
    "p3": ["2023-09-04", "2023-09-17"],
    "p4": ["2023-09-18", "2023-10-01"],
    "p5": ["2023-10-02", "2023-10-15"],
}

def handle_selection():
    selected_period = period_var.get()
    start_date, end_date = periods[selected_period]
    result_label.config(text=f"Selected period: {selected_period}, Start date: {start_date}, End date: {end_date}")

# Create the main application window
root = tk.Tk()
root.title("Choose Period")

# Create a guide label
guide_label = ttk.Label(root, text="请选择您想要收集的阶段:")
guide_label.pack(pady=10)

# Create a dropdown menu for the periods
period_var = tk.StringVar()
period_var.set(list(periods.keys())[0])  # Set the default value to the first period
period_dropdown = ttk.Combobox(root, textvariable=period_var, values=list(periods.keys()), state="readonly")
period_dropdown.pack(pady=5)

# Create a button to handle the selection
select_button = ttk.Button(root, text="确定", command=handle_selection)
select_button.pack(pady=5)

# Create a label to display the selection result
result_label = ttk.Label(root, text="")
result_label.pack(pady=10)

# Set the window title
root.title("Choose Period")

# Run the main event loop
root.mainloop()

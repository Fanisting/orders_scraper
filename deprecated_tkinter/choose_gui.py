import tkinter as tk
from tkinter import messagebox
from taobao import taobao
from jd import jd
from pdd import pdd


# Example functions (replace these with your actual functions)


def run_function(func):
    window.destroy()
    result = func()

# Create main window
window = tk.Tk()
window.title("请选择您想要收集数据的电商平台")
window.geometry("400x200")

# Create buttons for each function
taobao_button = tk.Button(window, text="淘宝/天猫", command=lambda: run_function(taobao))
taobao_button.pack(pady=10)

jd_button = tk.Button(window, text="京东", command=lambda: run_function(jd))
jd_button.pack(pady=10)

pdd_button = tk.Button(window, text="拼多多", command=lambda: run_function(pdd))
pdd_button.pack(pady=10)

window.mainloop()

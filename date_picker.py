from tkinter import *
import tkcalendar
from datetime import timedelta
from tkinter import messagebox

# Declare global variables for start_date and end_date
start_date = None
end_date = None

def pick_dates():
    global start_date, end_date

    root = Tk()
    root.title(u"日期选择")
    root.geometry("500x200")  # Set window size to 500x300 pixels

    guidance_label = Label(root, text="请选取开始和结束日期：")
    guidance_label.pack(padx=10, pady=10)

    def date_range(start, stop):
        global start_date, end_date

        # Check if start date is later than end date
        if start > stop:
            messagebox.showerror("错误", "确保开始日期早于结束日期")
        else:
            start_date = start
            end_date = stop
            print(f'开始日期：{start_date}\n结束日期：{end_date}')
            root.destroy()  # Close the tkinter window

    date1 = tkcalendar.DateEntry(root)
    date1.pack(padx=10, pady=10)

    date2 = tkcalendar.DateEntry(root)
    date2.pack(padx=10, pady=10)

    Button(root, text='查询范围', command=lambda: date_range(date1.get_date(), date2.get_date())).pack()

    root.mainloop()

    # Return start_date and end_date
    return start_date, end_date

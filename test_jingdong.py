from playwright.sync_api import sync_playwright
from pathlib import Path
import time
import os
import sys
from datetime import datetime
import logging
import tkinter as tk
from tkinter import messagebox
from date_picker import pick_dates

def setup_logger(log_file):
    # Create a logger
    logger = logging.getLogger('jingdong_logger')
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set the level to INFO
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Create a formatter to define the log message format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

def main():
    # Initialize the logger
    current_date = datetime.now().strftime('%Y-%m-%d')
    logger = setup_logger(f'jingdong_{current_date}.log')

    # Date management
    # determine whether to scrape next-page
    try:
        # select date range in calendar
        start_date, end_date = pick_dates()
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口，只显示弹窗
        root.attributes("-topmost", True)
        messagebox.showinfo("日期选择结果", f"开始日期：{start_date}\n结束日期：{end_date}")
        logger.info(f'chosen date range: {start_date} - {end_date}')
    except Exception as e:
        logger.info(f'{str(e)}')
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口，只显示弹窗
        root.attributes("-topmost", True)
        messagebox.showinfo("错误", "日期有误!")
        root.destroy()

    # Main program
    try:
        logger.info('Starting the program')
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # set default timeout
            page.set_default_timeout(120000)

            # Step 1: Open the link and login
            # pop up message
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口，只显示弹窗
            root.attributes("-topmost", True)
            messagebox.showinfo("开始操作", "我们将自动为您打开京东网页，请扫码登录您的京东账号!")
            root.destroy()
            logger.info('Showed message popup')
            # open link and wait until page loaded
            page.goto('https://order.jd.com/center/list.action')
            page.wait_for_load_state()
            logger.info('Login page already loaded')
            
            page.wait_for_selector('[id="order02"]', state="visible")
            logger.info('Go to orders page')
            # # Find more-functions button and click

            # # Click on the input element to open the calendar
            # page.locator('button.search-mod__more-button___nbIba').click()
            # page.wait_for_selector('[data-reactid=".0.2.1.0.1.1"]', state="visible")
            # # Click start date
            # page.locator('[data-reactid=".0.2.1.0.1.1"]').click()
            # page.wait_for_selector('a.rc-calendar-month-select', state="visible")
            # # Click start date in calendar
            # page.locator('a.rc-calendar-month-select').click() # months
            # page.wait_for_selector('div.rc-calendar-month-panel', state="visible")

            # # Now, let's say you want to select the date '2023-08-10'.
            # # You can construct the selector dynamically based on the desired date.
            # date_to_select = '2023-01-10'
            # year, month, day = date_to_select.split('-')
            # month_dict = {
            #     1: "一月",
            #     2: "二月",
            #     3: "三月",
            #     4: "四月",
            #     5: "五月",
            #     6: "六月",
            #     7: "七月",
            #     8: "八月",
            #     9: "九月",
            #     10: "十月",
            #     11: "十一月",
            #     12: "十二月"
            # }
            # month_selector = f'[title="{month_dict[int(month)]}"]'
            # page.locator(month_selector).click()
            # page.wait_for_selector('div.rc-calendar-calendar-body', state="visible")

            # # Select the date
            # date_selector = f'td[title="{int(year)}-{int(month)}-{int(day)}"]'
            # page.locator(date_selector).click()
            # page.wait_for_selector('a.rc-calendar-ok-btn', state="visible")
            # page.locator('a.rc-calendar-ok-btn').click()

            # time.sleep(5)

            # date_to_select_end = '2023-08-01'
            # year, month, day = date_to_select_end.split('-')            

            # page.wait_for_selector('[data-reactid=".0.2.1.0.1.3"]', state="visible")
            # # Click start date
            # page.locator('[data-reactid=".0.2.1.0.1.3"]').click()
            # page.wait_for_selector('a.rc-calendar-month-select', state="visible")
            # # Click start date in calendar
            # page.locator('a.rc-calendar-month-select').click() # months
            # page.wait_for_selector('div.rc-calendar-month-panel', state="visible")

            # month_selector = f'[title="{month_dict[int(month)]}"]'
            # page.locator(month_selector).click()
            # page.wait_for_selector('div.rc-calendar-calendar-body', state="visible")

            # # Select the date
            # date_selector = f'td[title="{int(year)}-{int(month)}-{int(day)}"]'
            # page.locator(date_selector).click()
            # page.wait_for_selector('a.rc-calendar-ok-btn', state="visible")
            # page.locator('a.rc-calendar-ok-btn').click()

            # Click search
            # time.sleep(2)
            # search_button_selector = 'button.button-mod__primary___1tmFA'
            # print(f"==>> search_button_selector: {search_button_selector}")
            # page.wait_for_selector(search_button_selector, state="visible")
            # print(f"==>> search_button_selector find: {search_button_selector}")
            # page.locator(search_button_selector).click()
            # print(f"==>> search_button_selector click: {search_button_selector}")

            # time.sleep(10)

            def update_next_link():
                link = "stop"
                next_button = page.query_selector('.next-disabled')
                # If 'next-disabled' doesn't exist, try to find the 'next' element
                if not next_button:
                    next_button = page.query_selector('.next')
                    link = "https:" + next_button.get_attribute('href')
                return link
            
            # Store once
            def store_html():
                element = page.locator('div[id="order02"]')
                html_content = element.inner_html()
                file.write(html_content)
             
            output_html = f"jingdong_{current_date}.html"
            with open(output_html, "w", encoding="utf-8") as file:
                store_html()
                link = update_next_link()
                while link != "stop":
                    page.goto(link)
                    page.wait_for_load_state()
                    store_html()
                    link = update_next_link()
                
            context.close()
            browser.close()
            logger.info('Closed the browser')

            

            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口，只显示弹窗
            root.attributes("-topmost", True)
            messagebox.showinfo("完成", "数据已经收集完毕!")
            root.destroy()
            logger.info('Showed finished message')

        logger.info('Completed successfully')
    except Exception as e:
            # Log exceptions or errors
            logger.error(f'Error occurred: {str(e)}')
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口，只显示弹窗
            root.attributes("-topmost", True)
            messagebox.showinfo("出现错误", f"{str(e)}")
            root.destroy()  # 销毁弹窗
    
if __name__ == "__main__":
    main()

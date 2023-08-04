from playwright.sync_api import sync_playwright
from pathlib import Path
import openpyxl
from openpyxl.utils import get_column_letter
import time
import os
import sys
from datetime import datetime
import logging
import tkinter as tk
from tkinter import messagebox
from date_picker import pick_dates
from parse_taobao import parse_date_range

def setup_logger(log_file):
    # Create a logger
    logger = logging.getLogger('taobao_logger')
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
    logger = setup_logger(f'taobao_{current_date}.log')

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
            messagebox.showinfo("开始操作", "我们将自动为您打开淘宝网页，请扫码登录您的淘宝账号!")
            root.destroy()
            logger.info('Showed message popup')
            # open link and wait until page loaded
            page.goto('https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm')
            page.wait_for_load_state()
            logger.info('Login page already loaded')

            # Step 2: Wait for login
            page.wait_for_selector('#bought', state="visible")
            page.wait_for_load_state("domcontentloaded")
            logger.info('Bought items page already loaded')

            def generate_html_file(id):
                output_dir = Path(sys.executable).parent
                output_folder = output_dir / "输出"
                output_folder.mkdir(exist_ok=True)
                output_html = output_folder / f"taobao_{current_date}_{id}.html"
                with open(output_html, "w", encoding="utf-8") as file:
                    file.write(html_content)
            
            # Step 4: extract data in other pages           
            def stop_rule(id, start_date, end_date):
                page_path = Path(sys.executable).parent / "输出" / f"taobao_{current_date}_{id}.html"
                first_date, last_date = parse_date_range(page_path)
                if first_date is not None:
                    first_date_obj = datetime.strptime(first_date, "%Y-%m-%d").date()
                    last_date_obj = datetime.strptime(last_date, "%Y-%m-%d").date()
                    # category by end date
                    if end_date > first_date_obj: 
                        # the most recent order is outdated
                        # we have already stored first page
                        return False
                    elif start_date > last_date_obj: 
                        # orders are only the part of page 1
                        return False
                    else:
                        # scrape next-page content
                        return True
                else:
                    return False
            
            stop = False
            id = 1
            while not stop:
                print('while starts')
                if id >= 2:
                    # Store current order number
                    orderNums = page.query_selector_all('//div/table/tbody/tr/td/span/span[3]')
                    first_orderNum = orderNums[0].get_attribute('innerText')
                    print(f"==>> first_orderNum: {first_orderNum}")

                    # Find and click next page button is nat disabled
                    next_button = page.locator('button:has-text("下一页")')
                    print('check button')
                    is_disabled = next_button.is_disabled()
                    if is_disabled:
                        print(f"==>> is_disabled: True")
                        break
                    else:
                        next_button.click()
                    
                    # Listen to changes of page
                    def orderNum_updated():
                        time.sleep(2)
                        orderNums = page.query_selector_all('//div/table/tbody/tr/td/span/span[3]')
                        new_orderNum = orderNums[0].get_attribute('innerText')
                        return new_orderNum
                    while True:
                        new_orderNum = page.evaluate(orderNum_updated())
                        if first_orderNum != new_orderNum:
                            print("Element has changed")
                            break
                        first_orderNum = new_orderNum
                        time.sleep(2)
                    
                html_content = page.content()
                generate_html_file(id)
                
                stop = stop_rule(id, start_date, end_date)
                id += 1

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
            logger.error(f'An error occurred: {str(e)}')
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口，只显示弹窗
            root.attributes("-topmost", True)
            messagebox.showinfo("出现错误", f"{str(e)}")
            root.destroy()  # 销毁弹窗
    
if __name__ == "__main__":
    main()


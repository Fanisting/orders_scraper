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
                element = page.locator('div[id="tp-bought-root"]')
                html_content = element.inner_html()
                output_dir = Path(sys.executable).parent
                output_folder = output_dir / "输出"
                output_folder.mkdir(exist_ok=True)
                output_html = output_folder / f"taobao_{current_date}_{id}.html"
                with open(output_html, "w", encoding="utf-8") as file:
                    file.write(html_content)
            
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

            results = page.query_selector_all('.pagination-item')
            results_num = len(results)
            print(f"==>> results_num: {results_num}")

            def watch_for_change(id, page, xpath, timeout=30):
                # assume now we are in page-id
                current_value = page.eval_on_selector(f'xpath={xpath}', 'element => element.textContent')
                print(f"==>> current_value: {current_value}")
                # click to next page
                page.locator(f'li.pagination-item-{id+1}').click()
                time.sleep(5)

                start_time = time.time()
                while time.time() - start_time < timeout:
                    new_value = page.eval_on_selector(f'xpath={xpath}', 'element => element.textContent')
                    print(f"==>> new_value: {new_value}")
                    if new_value != current_value:
                        print(f"Page navigated to {id+1}")
                        time.sleep(2)
                        break
                    time.sleep(1)  # wait for 0.5 seconds before checking again

                return None
            
            output_html = f"taobao_{current_date}.html"

            def store_html():
                element = page.locator('div[id="tp-bought-root"]')
                html_content = element.inner_html()
                file.write(html_content)            
            with open(output_html, "w", encoding="utf-8") as file:
                if results_num == 1:
                    print("only one page detected")
                    logger.info(f'only one page detected')
                    store_html()
                    logger.info(f'Finished writing page 1')
                else:
                    for i in range(1, results_num):
                        file.write(f"Page {i}\n")
                        logger.info(f'Start writing page {i}')
                        store_html()
                        logger.info(f'Finished writing page {i}')
                        watch_for_change(i, page, "//div/table/tbody/tr/td/span/span[3]")
                        logger.info(f'Finished page navigation {i}')
                    logger.info(f'Start writing page {results_num}')
                    file.write(f"Page {results_num}\n")
                    store_html()
                    logger.info(f'Finished writing page {results_num}')
                    # generate_html_file(results_num)
                
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

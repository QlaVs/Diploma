"""
TODO:
    1. Log Analyzer
    2. Visualize log data to expert
"""

import json
import time
import logging
import threading
from read_screen import Reader
from selenium import webdriver

logging.getLogger().setLevel(logging.INFO)
# logging.basicConfig(filename="LogFile.log",
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG)

driver = webdriver.Firefox()
driver.get("http://www.google.com")
tabs = 1

f = open('Lists.JSON')
lists = json.load(f)
curr_url = "about:blank"

logging.info("Program is starting up...")

reader = Reader()
reader_thread = threading.Thread(target=reader.start, name="RR")
reader_thread.start()

while True:
    try:
        time.sleep(1)
        url = driver.current_url
        if url != curr_url:
            logging.info("URL Changed: " + url)
            for i in lists['bl']:
                if i in url:
                    logging.error("Black List URL, redirecting...")
                    driver.back()
                    break
            else:
                if reader.get_status():
                    reader.change_status(False)
                curr_url = url
                for i in lists['wl']:
                    if i in url:
                        logging.info("White List URL")
                        break
                else:
                    logging.warning("Not in Lists, monitoring...")
                    reader.change_status(True)

        # print(driver.window_handles)
        # if tabs != len(driver.window_handles):
        # print("Urls list:")
        # driver.execute_script("return document.visibilityState") == "visible"
        # temp = driver.current_window_handle
        # print("Change")
        # print(temp)
        # for handle in driver.window_handles:
        #     driver.switch_to.window(handle)
        #     print(driver.current_url)
        # tabs = len(driver.window_handles)
        #
        # print("Current data:")
        # print(driver.current_url)
        # print(driver.current_window_handle)
        # print("--------------------------------------------------")
        # driver.switch_to(driver.current_window_handle)

    except:
        try:
            main_page = driver.window_handles[0]
            driver.switch_to.window(main_page)

        except:
            print("Browser closed")
            reader.stop()
            exit(0)

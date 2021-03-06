"""
TODO:
    1. Log Analyzer
    2. Visualize log data to expert
"""

import json
from urllib.parse import urlparse
import time
import logging
import threading
from log_analyzer import Analyzer
from read_screen import Reader
from selenium import webdriver


# try:
#     with open('LogFile.log', 'w'):
#         pass
# except:
#     pass

logging.getLogger("scanner")
logging.basicConfig(filename="LogFile.log",
                    filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

tabs = 1

driver = webdriver.Firefox()
driver.get("http://www.google.com")
with open('Lists.JSON') as f:
    lists = json.load(f)

curr_url = "about:blank"

logging.info("Program is starting up...")


# nf = Notifier()
# notifier_thread = threading.Thread(target=nf.start, name="NF")
# notifier_thread.start()

reader = Reader(driver)
reader_thread = threading.Thread(target=reader.start, name="RR")
reader_thread.start()

while True:
    try:
        time.sleep(0.5)
        url = driver.current_url
        # url = re.search('//(.*?)/', url)
        # url = url.group(1)
        url = urlparse(url)
        url = url.netloc
        if url != curr_url:
            logging.info("URL Changed: " + url)
            for i in lists['bl']:
                if i in url:
                    logging.warning("Black List URL, redirecting...")
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
                    # notification = re.search('//(.*?)/', curr_url) notification.group(1)
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
            logging.info("Browser closed")
            reader.stop()

            analyzer = Analyzer("LogFile.log")
            analyzer.start()

            print('Exiting...')
            exit(0)

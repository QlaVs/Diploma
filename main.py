import json
import time
from read_screen import Reader
from selenium import webdriver

driver = webdriver.Firefox()
tabs = 1
f = open('Lists.JSON')
lists = json.load(f)
curr_url = "about:blank"

print("Working...")

reader = Reader()
print("Reader Created")

while True:
    try:
        time.sleep(1)
        url = driver.current_url
        if url != curr_url:
            if reader.get_status():
                reader.change_status(False)
            print("URL Changed: " + url)
            for i in lists['bl']:
                if i in url:
                    print("[ERR] Black List URL, redirecting...")
                    driver.back()
                    break
            else:
                curr_url = url
                for i in lists['wl']:
                    if i in url:
                        print("[OK] White List URL")
                        break
                else:
                    print("[WRNG] Not in Lists, monitoring...")
                    reader.change_status(True)
                    reader.start()


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
        main_page = driver.window_handles[0]
        driver.switch_to.window(main_page)

import time
import ML
import mss
import numpy
import re
import json
import pytesseract
import logging
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier

# pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
# mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

f = open('Words.JSON', encoding='utf-8')
words = json.load(f)

f = open('phishing_cites.json')
cites_list = json.load(f)


class Reader:
    state = False
    stopping = False

    def __init__(self, driver):
        self.driver = driver

    def change_status(self, state):
        if state != self.state:
            self.state = state

    def get_status(self):
        return self.state

    def start(self):
        print("Scanner online")
        while not self.state:
            pass
            # if self.stopping:
            #     print("Scanner stopped")
            #     return
        try:
            print("Start scanning...")
            # with mss.mss() as sct:
            while self.state:
                if self.stopping:
                    logging.info("Scanner stopped")
                    return

                # im = numpy.asarray(sct.grab(mon))
                #
                # text = pytesseract.image_to_string(im, lang="rus")

                try:
                    phishing = 0

                    curr_url = re.search('//(.*?)/', self.driver.current_url)
                    curr_url = curr_url.group(1)

                    for i in range(len(cites_list)):
                        phish_url = re.search('//(.*?)/', cites_list[i]["url"])
                        if phish_url:
                            phish_url = phish_url.group(1)
                            # print(phish_url)
                            if phish_url == curr_url:
                                phishing = 1
                                break

                    ML.check_strings(self.driver.page_source, words, phishing)

                except Exception as err:
                    print(err)

                # for i in words:
                    # TODO: Create field disabling feature

                    # try:
                    #     z = self.driver.find_element(By.CSS_SELECTOR, f'input[id*={i}]')
                    #     # z = self.driver.find_element(By.XPATH, f"text()[contains(.,'{i}')]")
                    #     # z = self.driver.find_element(By.XPATH, f".//*[input()='{i}']")
                    #     logging.warning("Suspicious word (id): " + i)
                    # except:
                    #     pass
                    #
                    # try:
                    #     x = self.driver.find_element(By.CSS_SELECTOR, f'input[name*={i}]')
                    #     logging.warning("Suspicious word (name): " + i)
                    # except:
                    #     pass
                    #
                    # try:
                    #     y = self.driver.find_element(By.CSS_SELECTOR, f'input[class*={i}]')
                    #     logging.warning("Suspicious word (class): " + i)
                    # except:
                    #     pass



                # else:
                print("Checking")
                #     if i in text:
                #         logging.warning("Suspicious word: " + i)

                time.sleep(5)
            self.start()
        except Exception as err:
            return logging.critical(err)

    def stop(self) -> None:
        if not self.stopping:
            self.stopping = not self.stopping


class Notifier:
    stopping = False
    url = None

    def __init__(self):
        self.toast = ToastNotifier()

    def start(self):
        print("Notifier online")
        while True:
            try:
                if self.stopping:
                    logging.info("Notifier stopped")
                    return
                if self.url is not None:
                    self.toast.show_toast("Небезопасный сайт",
                                          f"{self.url} может быть использован для кражи персональных данных\n"
                                          "Пожалуйста, не вводите личные данные на этой странице",
                                          duration=7)
                    self.url = None
            except Exception as err:
                return logging.critical(err)

    def notification(self, url):
        self.url = url

    def stop(self) -> None:
        if not self.stopping:
            self.stopping = not self.stopping

import time
import mss
import numpy
import pytesseract
import logging
from selenium.webdriver.common.by import By

# pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
# mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

f = open('Words.txt', 'r', encoding='utf-8')
words = f.read().splitlines()


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
        print("Scanner is waiting")
        while not self.state:
            if self.stopping:
                print("Scanner stopped")
                return
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

                for i in words:
                    # TODO: Create field disabling feature
                    try:
                        z = self.driver.find_element(By.CSS_SELECTOR, f'input[id*={i}]')
                        # z = self.driver.find_element(By.XPATH, f"text()[contains(.,'{i}')]")
                        # z = self.driver.find_element(By.XPATH, f".//*[input()='{i}']")
                        logging.warning("Suspicious word (id): " + i)
                    except:
                        pass

                    try:
                        x = self.driver.find_element(By.CSS_SELECTOR, f'input[name*={i}]')
                        logging.warning("Suspicious word (name): " + i)
                    except:
                        pass

                    try:
                        y = self.driver.find_element(By.CSS_SELECTOR, f'input[class*={i}]')
                        logging.warning("Suspicious word (class): " + i)
                    except:
                        pass

                else:
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

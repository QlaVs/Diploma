import threading
import time
import traceback
from urllib.parse import urlparse
import requests
import ML
import json
import logging
from win10toast import ToastNotifier

# pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
# mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}\


with open('Words.JSON', encoding='utf-8') as wf:
    words = json.load(wf)

with open('phishing_cites.json') as cf:
    cites_list = json.load(cf)


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
                    self.toast.show_toast("Потенциальная угроза",
                                          f"{self.url} может быть использован для кражи персональных данных\n"
                                          "Пожалуйста, не вводите личные данные на этой странице",
                                          duration=10)
                    self.url = None
                time.sleep(0.2)
            except Exception as err:
                return logging.critical(err)

    def notification(self, url):
        self.url = url
        # self.toast.show_toast("Потенциальная угроза",
        #                       f"{self.url} может быть использован для кражи персональных данных\n"
        #                       "Пожалуйста, не вводите личные данные на этой странице",
        #                       duration=10)

    def stop(self) -> None:
        if not self.stopping:
            self.stopping = not self.stopping


nf = Notifier()
notifier_thread = threading.Thread(target=nf.start, name="NF")
notifier_thread.start()


class Reader:
    state = False
    stopping = False
    html_page = ''
    temp_url = ''

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
                    sus = -1

                    # curr_url = re.search('//(.*?)/', self.driver.current_url)
                    # curr_url = curr_url.group(1)

                    curr_url = urlparse(self.driver.current_url)
                    if curr_url.scheme != "https":
                        sus = 1
                    curr_url = curr_url.netloc

                    # This is where the magic taking place!
                    if self.temp_url != curr_url or self.html_page != self.driver.page_source:
                        self.temp_url = curr_url
                        self.html_page = self.driver.page_source

                        # temp = re.findall('(?<=\.)\w+(?=\.)', curr_url)
                        temp = curr_url.split('.')
                        if sus != 1:
                            if len(temp) != 3:
                                sus = 0
                            elif temp[0] != 'www' or temp[2] not in words['domain']:
                                sus = 1

                        for i in range(len(cites_list)):
                            # phish_url = re.search('//(.*?)/', cites_list[i]["url"])
                            phish_url = urlparse(cites_list[i]['url'])
                            phish_url = phish_url.netloc
                            # phish_url = phish_url.group(1)
                            # print(phish_url)
                            if phish_url == curr_url:
                                phishing = 1
                                break

                        rank_data = requests.get(
                            f'https://openpagerank.com/api/v1.0/getPageRank?API-OPR'
                            f'=kco0goc4cwwgcog0ok08ckscsw0kcck0wg4840wg&domains[]={curr_url}')

                        r = rank_data.json()['response'][0]['page_rank_decimal']

                        if r <= 3.36:
                            rank = -1
                        elif r <= 7.33:
                            rank = 0
                        else:
                            rank = 1

                        rank_data = requests.get(
                            f'https://ipqualityscore.com/api/json/url/y5ag8EOGiHiBm8t5jxzRuR4D86C7Jz1t/{curr_url}')

                        r = rank_data.json()
                        if not r['phishing']:
                            iqs_phishing = 0
                        else:
                            iqs_phishing = 1

                        if not r['suspicious']:
                            iqs_sus = 0
                        else:
                            iqs_sus = 1

                        if r['risk_score'] <= 33:
                            iqs_risk_score = -1
                        elif r['risk_score'] <= 66:
                            iqs_risk_score = 0
                        else:
                            iqs_risk_score = 1

                        result = ML.check_strings(
                            self.html_page, words, phishing, rank, sus, iqs_phishing, iqs_sus, iqs_risk_score)

                        if result == 1:
                            nf.notification(curr_url)
                        elif result == -1:
                            print("Might not be phishing page")
                        elif result == 0:
                            print("Waiting for changes")

                        temp.clear()
                    else:
                        print("Page was already checked")

                except Exception:
                    print(traceback.format_exc())

                # for i in words:
                # TODO: Create field disabling feature

                # try:
                #     z = self.driver.find_element(By.CSS_SELECTOR, f'input[id*={i}]')
                #     z = self.driver.find_element(By.XPATH, f"text()[contains(.,'{i}')]")
                #     z = self.driver.find_element(By.XPATH, f".//*[input()='{i}']")
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
            nf.stop()
            self.stopping = not self.stopping

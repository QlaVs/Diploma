import time
import mss
import numpy
import pytesseract
import logging

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

f = open('Words.txt', 'r', encoding='utf-8')
words = f.readlines()


class Reader:
    state = False
    stopping = False

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
            with mss.mss() as sct:
                while self.state:
                    if self.stopping:
                        print("Scanner stopped")
                        return
                    im = numpy.asarray(sct.grab(mon))

                    text = pytesseract.image_to_string(im, lang="rus")

                    for i in words:
                        if i in text:
                            logging.warning("Suspicious word: " + i)

                    time.sleep(5)
                self.start()
        except Exception as err:
            return "[ERR]" + str(err)

    def stop(self) -> None:
        if not self.stopping:
            self.stopping = not self.stopping

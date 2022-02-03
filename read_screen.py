import time
import mss
import numpy
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

f = open('Words.txt', 'r', encoding='utf-8')
words = f.readlines()


class Reader:
    state = False

    def change_status(self, state):
        if state != self.state:
            self.state = state

    def get_status(self):
        return self.state

    def start(self):
        with mss.mss() as sct:
            while self.state:
                im = numpy.asarray(sct.grab(mon))

                text = pytesseract.image_to_string(im, lang="rus")

                for i in words:
                    if i in text:
                        print("[WRNNG] Suspicious word:" + i)

                time.sleep(5)

            print("Stop Working...")

import time
import cv2
import mss
import numpy
import pytesseract


mon = {'top': 0, 'left': 0, 'width': 150, 'height': 150}

with mss.mss() as sct:
    while True:
        im = numpy.asarray(sct.grab(mon))
        # im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(im)
        print(text)

        cv2.imshow('Image', im)

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        # One screenshot per second
        time.sleep(1)

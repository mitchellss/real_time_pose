
import os

import cv2
from constants.constants import PATH

class Demo():

    def __init__(self, activity) -> None:
        self.path = PATH / "activities" / activity / "demo.mp4"
        self.file_exists = os.path.exists(self.path)
        if self.file_exists:
            self.cap = cv2.VideoCapture(str(self.path))

    def get_image(self):
        if self.file_exists:
            ret, frame = self.cap.read()
            if ret == True:
                img = cv2.resize(frame, (750,500))
                return img

    def stop(self):
        if self.file_exists:
            self.cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    demo = Demo("jumping_jacks")
    demo.play()

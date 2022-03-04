
from constants.constants import PATH
from data_logging.logger import Logger
import time


class CSVPointLogger(Logger):

    def __init__(self, fname, **kwargs) -> None:
        super().__init__(fname)

    def log(self, data):
        if self.logging:
            self.point_file.write(str(time.time()) + "," + ','.join([f"{num[0]},{num[1]}" for num in data]) + "\n")

    def new_log(self):
        if self.logging:
            self.close()
        self.current_time = int(time.time())
        self.point_file = open(PATH / "data" / self.folder_name / f"{self.current_time}_{self.fname}.csv", "w")
        self.point_file.write("timestamp,x00,y00,x01,y01,x02,y02,\
x03,y03,x04,y04,x05,y05,x06,y06,x07,y07,x08,y08,x09,y09,x10,\
y10,x11,y11,x12,y12,x13,y13,x14,y14,x15,y15,x16,y16,x17,y17,\
x18,y18,x19,y19,x20,y20,x21,y21,x22,y22,x23,y23,x24,y24,x25,\
y25,x26,y26,x27,y27,x28,y28,x29,y29,x30,y30,x31,y31,x32,y32\n")

    def close(self):
        self.point_file.close()
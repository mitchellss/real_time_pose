
import numpy as np
import pandas as pd
from constants.constants import PATH
from data_logging.logger import Logger
import time


class CSVPointLogger(Logger):

    def __init__(self, fname, **kwargs) -> None:
        super().__init__(fname)
        self.data = np.zeros((0,133))

    def log(self, data):
        newdata = data.ravel() # Make array 1D
        newdata = np.insert(newdata, 0, [time.time()]) # Insert time into first column
        if self.logging:
            self.data = np.vstack([self.data, newdata])

    def new_log(self):
        if self.logging:
            self.close()
        self.current_time = int(time.time())
        self.data = np.zeros((0,133))

    def stop_logging(self):
        np.savetxt(PATH / "data" / self.folder_name / f"{self.current_time}_{self.fname}.csv", 
        self.data, delimiter=",", header="timestamp,x00,y00,z00,vis00,\
x01,y01,z01,vis01,x02,y02,z02,vis02,x03,y03,z03,vis03,x04,y04,z04,vis04,\
x05,y05,z05,vis05,x06,y06,z06,vis06,x07,y07,z07,vis07,x08,y08,z08,vis08,\
x09,y09,z09,vis09,x10,y10,z10,vis10,x11,y11,z11,vis11,x12,y12,z12,vis12,\
x13,y13,z13,vis13,x14,y14,z14,vis14,x15,y15,z15,vis15,x16,y16,z16,vis16,\
x17,y17,z17,vis17,x18,y18,z18,vis18,x19,y19,z19,vis19,x20,y20,z20,vis20,\
x21,y21,z21,vis21,x22,y22,z22,vis22,x23,y23,z23,vis23,x24,y24,z24,vis24,\
x25,y25,z25,vis25,x26,y26,z26,vis26,x27,y27,z27,vis27,x28,y28,z28,vis28\
,x29,y29,z29,vis29,x30,y30,z30,vis30,x31,y31,z31,vis31,x32,y32,z32,vis32",
comments="", fmt="%.5f")
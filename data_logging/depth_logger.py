
import numpy as np
import pandas as pd
from constants.constants import PATH
from data_logging.logger import Logger
import time


class DepthLogger(Logger):

    def __init__(self, fname, **kwargs) -> None:
        super().__init__(fname)
        self.data = np.zeros((480,640))

    def log(self, data):
        if self.logging:
            self.data = np.vstack([self.data, data])

    def new_log(self):
        if self.logging:
            self.close()
        self.current_time = int(time.time())
        self.data = np.zeros((480,640))

    def stop_logging(self):
        np.savetxt(PATH / "data" / self.folder_name / f"{self.current_time}_{self.fname}_depth.csv", 
        self.data, delimiter=",", comments="", fmt="%.5f")
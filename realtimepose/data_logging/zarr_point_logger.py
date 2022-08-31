
from constants.constants import PATH
import time
import zarr
import numpy as np
import pandas as pd



class ZarrLogger:

    def __init__(self, fname) -> None:
        super().__init__(fname)
        self.data = np.zeros((0,133))

    def log(self, data: np.ndarray):
        newdata = data.ravel() # Make array 1D
        newdata = np.insert(newdata, 0, [time.time()]) # Insert time into first column
        if self.logging:
            self.data = np.vstack([self.data, newdata])

    def new_log(self):
        if self.logging:
            self.close()
        self.current_time = int(time.time())
        self.data = np.zeros((0,133))

    def stop_logging(self) -> None:
        # df = pd.DataFrame(self.data)
        # df.to_csv(PATH / "data" / self.folder_name / f"{self.current_time}_{self.fname}.csv")
        zarr.save(PATH / "data" / self.folder_name / f"{self.current_time}_{self.fname}.zarr", self.data)

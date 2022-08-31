
from constants.constants import PATH
import time
import h5py
import numpy as np
import pandas as pd



class Hdf5Logger:

    def __init__(self, fname) -> None:
        super().__init__(fname)
        self.data = np.zeros((0,133))
        h5_filename = f"{str(self.current_time)}.h5"
        self.h5f = h5py.File(PATH / "data" / self.folder_name / h5_filename,'w')

    def log(self, data: np.ndarray):
        if self.logging:
            newdata = data.ravel() # Make array 1D
            newdata = np.insert(newdata, 0, [time.time()]) # Insert time into first column
            self.data = np.vstack([self.data, newdata])
            
    def close(self):
        self.h5f.create_dataset(str(self.current_time), data=self.data, dtype=np.float64)

    def new_log(self):
        self.current_time = int(time.time())
        self.data = np.zeros((0,133))

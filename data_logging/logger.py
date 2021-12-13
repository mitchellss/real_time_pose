import os
from constants.constants import PATH

class Logger():

    def __init__(self, fname, **kwargs) -> None:
        if not os.path.isdir(PATH / "data" / fname):
            os.makedirs(PATH / "data" / fname)

    def log(self, data):
        pass

    def close(self):
        pass
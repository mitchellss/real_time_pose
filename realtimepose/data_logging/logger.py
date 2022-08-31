import os
import time
# from constants.constants import PATH
from typing_extensions import Protocol

class Logger(Protocol):

    # def __init__(self, fname) -> None:
    #     self.current_time = int(time.time())
    #     self.fname = fname
    #     self.logging = False
    #     self.folder_name = f"{self.fname}"

    #     if not os.path.isdir(PATH / "data" / self.folder_name):
    #         os.makedirs(PATH / "data" / self.folder_name)

    def log(self, **data) -> None:
        pass

    def new_log(self) -> None:
        pass

    def close(self) -> None:
        pass

    def start_logging(self) -> None:
        # self.logging = True
        pass

    def stop_logging(self) -> None:
        # self.logging = False
        pass

    def is_logging(self) -> bool:
        # return self.logging
        pass
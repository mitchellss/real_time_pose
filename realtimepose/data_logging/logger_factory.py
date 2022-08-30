

import sys
from data_logging.csv_point_logger import CSVPointLogger
from data_logging.hdf5_point_logger import Hdf5PointLogger
from data_logging.logger import Logger

from data_logging.video_logger import VideoLogger
from data_logging.zarr_point_logger import ZarrPointLogger


class LoggerFactory:
    
    def get_logger(self, logger_name:str, data_folder_name:str, **kwargs) -> Logger:
        if logger_name == "video":
            try:
                return VideoLogger(data_folder_name, frame_width=kwargs["frame_width"], 
                                frame_height=kwargs["frame_height"], fps=kwargs["fps"])
            except Exception as e:
                print("Must provide video logger height/width/fps")
                print(e)
                sys.exit(1)
        elif logger_name == "csv":
            return CSVPointLogger(data_folder_name)
        elif logger_name == "hdf5":
            return Hdf5PointLogger(data_folder_name)
        elif logger_name == "zarr":
            return ZarrPointLogger(data_folder_name)
        else:
            print("Invalid logger name")
            sys.exit(1)


import sys
from pose_detection.computer_vision.cv_model.blazepose import Blazepose
from pose_detection.computer_vision.cv_model.cv_model import CVModel


class CVModelFactory:

    def get_cv_model(cv_model_name:str) -> CVModel:
        if cv_model_name == "blazepose":
            return(Blazepose())
        else:
            print(f"Unrecognized computer vision model: {cv_model_name}")
            sys.exit(1)

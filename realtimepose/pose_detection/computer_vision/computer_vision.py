
import numpy as np

from pose_detection.computer_vision.cv_model.cv_model import CVModel
from pose_detection.computer_vision.cv_model.cv_model_factory import CVModelFactory

import cv2

class ComputerVision:
    
    def __init__(self, queue, cv_model_name: str, **kwargs) -> None:
        self.pose = None
        cv_model_factory = CVModelFactory()
        self.cv_model: CVModel = cv_model_factory.get_cv_model(cv_model_name)
    
    def get_skeleton(self, preprocessed_image: any) -> np.ndarray:
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        preprocessed_image.flags.writeable = False
        self.pose = self.cv_model.get_pose(preprocessed_image)
        preprocessed_image.flags.writeable = True
        return self.pose

    def _preprocess(self, frame: np.ndarray):
        return cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

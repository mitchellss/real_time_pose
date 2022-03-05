
from constants.constants import *
from pose_detection.computer_vision.cv_model.cv_model import CVModel
import numpy as np
import mediapipe as mp

class Blazepose(CVModel):
    """
    PoseDetector implementation of Google's BlazePose model
    
    Attributes:
        model_complexity: 0 for light, 1 for full, 2 for heavy
        min_detection_confidence: minimum detection confidence
        min_tracking_confidence: minimum tracking confidence
    """

    def __init__(self, *, model_complexity: int = 1,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5) -> None:
        super().__init__()

        self.mp_pose = mp.solutions.pose

        # Model complexity:
        # 0 : Light
        # 1 : Full
        # 2 : Heavy
        self.pose = self.mp_pose.Pose(min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence, model_complexity=model_complexity)

    def get_pose(self, image: np.ndarray) -> np.ndarray:
        landmarks = self.pose.process(image).pose_world_landmarks.landmark
        for landmark in range(0,len(landmarks)):
            # Save raw data for logging purposes
            self.skeleton_array[landmark][0] = landmarks[landmark].x
            self.skeleton_array[landmark][1] = landmarks[landmark].y
            self.skeleton_array[landmark][2] = landmarks[landmark].z
            self.skeleton_array[landmark][3] = landmarks[landmark].visibility
        return self.skeleton_array

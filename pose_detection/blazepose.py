
from pose_detection.pose_detection import PoseDetector
import numpy as np
import mediapipe as mp

class Blazepose(PoseDetector):
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
        self.mp_pose = mp.solutions.pose

        # Model complexity:
        # 0 : Light
        # 1 : Full
        # 2 : Heavy
        self.pose = self.mp_pose.Pose(min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence, model_complexity=model_complexity)

    def get_pose(self, image: np.ndarray) -> list:
        return self.pose.process(image).pose_world_landmarks
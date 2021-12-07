


from pose_detection.pose_detection import PoseDetector
import numpy as np
import mediapipe as mp

class Blazepose(PoseDetector):

    def __init__(self) -> None:
        self.mp_pose = mp.solutions.pose

        # Model complexity:
        # 0 : Light
        # 1 : Full
        # 2 : Heavy
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5,
                min_tracking_confidence=0.5, model_complexity=1)

    def get_pose(self, image: np.ndarray) -> list:
        return self.pose.process(image).pose_world_landmarks
"""Test"""
import logging
from typing import Any
import numpy as np
import mediapipe as mp


class BlazePose:
    """Test"""

    def __init__(self) -> None:
        self.pose_array = np.zeros((33, 4))
        self.mp_pose = mp.solutions.pose
        self.model = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity=0)

    # @timing
    def get_pose(self, frame: np.ndarray) -> np.ndarray:
        """Test"""
        try:
            landmarks = self.model.process(frame).pose_world_landmarks.landmark
            for landmark in range(0, len(landmarks)):
                # Save raw data for logging purposes
                self.pose_array[landmark][0] = landmarks[landmark].x
                self.pose_array[landmark][1] = landmarks[landmark].y
                self.pose_array[landmark][2] = landmarks[landmark].z
                self.pose_array[landmark][3] = landmarks[landmark].visibility
            return self.pose_array
        except:
            logging.warning("Error occured")
            return self.pose_array

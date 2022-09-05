"""Test"""
import logging
from typing import Any
import numpy as np
import mediapipe as mp


class BlazePose:
    """Test"""

    def __init__(self) -> None:
        self.pose_array = np.zeros((33, 4))
        self.mp_pose = mp.solutions.pose  # type: ignore
        self.model = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity=1)

    def get_pose(self, frame: np.ndarray) -> np.ndarray:
        """Test"""
        try:
            landmarks = self.model.process(frame)
            pose = landmarks.pose_world_landmarks.landmark
            for landmark in range(0, len(pose)):
                # Save raw data for logging purposes
                self.pose_array[landmark][0] = pose[landmark].x
                self.pose_array[landmark][1] = pose[landmark].y
                self.pose_array[landmark][2] = pose[landmark].z
                self.pose_array[landmark][3] = pose[landmark].visibility
            return self.pose_array
        except AttributeError:
            # This error is thrown when a pose is not found in the image provided
            return self.pose_array
        except KeyboardInterrupt as e:
            logging.info("Ctrl-C pressed...")
            raise(e)

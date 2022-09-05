"""Test"""
import numpy as np
import cv2


class Webcam:
    """Test"""

    def __init__(self, device_num) -> None:
        self.cap = cv2.VideoCapture(device_num)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))

    def get_frame(self) -> np.ndarray:
        """Test"""
        success, color_image = self.cap.read()
        if not success:
            return np.zeros(0)
        return color_image

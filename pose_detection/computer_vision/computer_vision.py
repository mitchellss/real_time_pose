
import numpy as np
from pose_detection.computer_vision.cv_model.cv_model import CVModel
from pose_detection.computer_vision.frame_input.frame_input import FrameInput
from pose_detection.pose_detection import PoseDetection
import cv2

class ComputerVision(PoseDetection):
    
    def __init__(self, cv_model: CVModel, frame_input: FrameInput, **kwargs) -> None:
        super().__init__()
        self.cv_model = cv_model
        self.frame_input = frame_input

        if "hide_video" in kwargs:
            self.hide_video = kwargs["hide_video"]
        else:
            self.hide_video = False
    
    def add_pose_to_queue(self) -> bool:

        frame: np.ndarray = self.frame_input.get_frame()
        image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        self.pose = self.cv_model.get_pose(image)
        image.flags.writeable = True

        if not self.hide_video:
            image2 = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imshow("MediaPipe Pose", image2)

        if cv2.waitKey(5) & 0xFF == 27:
            return False

        super().add_pose_to_queue()
        return True
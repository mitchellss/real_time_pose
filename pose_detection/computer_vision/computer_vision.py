
import numpy as np
from data_logging.video_logger import VideoLogger
from pose_detection.computer_vision.cv_model.cv_model import CVModel
from pose_detection.computer_vision.frame_input.frame_input import FrameInput
from pose_detection.pose_detection import PoseDetection
import cv2

class ComputerVision(PoseDetection):
    
    def __init__(self, queue, cv_model: CVModel, frame_input: FrameInput, **kwargs) -> None:
        super().__init__(queue)
        self.cv_model = cv_model
        self.frame_input = frame_input

        if "hide_video" in kwargs:
            self.hide_video = kwargs["hide_video"]
        else:
            self.hide_video = False

        if "record_video" in kwargs:
            self.video_logger, self.depth_logger = kwargs["record_video"]
        else:
            self.video_logger = None

        # if self.video_logger != None:
        #     self.video_logger.new_log()
    
    def add_pose_to_queue(self) -> bool:

        color_frame, depth_frame = self.frame_input.get_frame()
        image = cv2.cvtColor(cv2.flip(color_frame, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        self.pose = self.cv_model.get_pose(image)
        image.flags.writeable = True

        image2 = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if self.video_logger != None:
            self.video_logger.log(image2)
            self.depth_logger.log(depth_frame)

        if not self.hide_video:
            cv2.imshow("MediaPipe Pose", image2)

        if cv2.waitKey(5) & 0xFF == 27:
            return False

        super().add_pose_to_queue()
        return True
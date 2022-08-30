

from pose_detection.computer_vision.computer_vision import ComputerVision
from pose_detection.pose_detection import PoseDetection
from pose_detection.vicon.vicon import Vicon


class PoseDetectionFactory:
    
    def get_pose_detection(self, input:str, queue:str, cv_model_name: str) -> PoseDetection:
        if input == "video":
            return(ComputerVision(queue=queue, cv_model_name=cv_model_name))
        elif input =="vicon":
            return(Vicon(queue=queue))
        

from pose_detection.pose_detection import PoseDetection


class Vicon(PoseDetection):

    def __init__(self, queue) -> None:
        super().__init__(queue)
        
    pass

import argparse
import os
import sys
import time

import cv2
from data_logging.video_logger import VideoLogger
from pose_detection.computer_vision.computer_vision import ComputerVision

from pose_detection.computer_vision.cv_model.blazepose import Blazepose
from pose_detection.computer_vision.frame_input.frame_input import FrameInput
from pose_detection.computer_vision.frame_input.realsense import Realsense
from pose_detection.computer_vision.frame_input.video_file_input import VideoFileInput
from pose_detection.computer_vision.frame_input.webcam import Webcam
from pose_detection.pose_detection import PoseDetection
from pose_detection.vicon.vicon import Vicon


class PoseService:

    def __init__(self, input="video", video_input="webcam", path=".", record_video=False, queue="redis", hide_video=False) -> None:
                
        self.pose_detection: PoseDetection = None
        self.frame_input: FrameInput = None
        self.cont = True

        if input == "video":
            # Select video input method
            if video_input == "file":
                self.frame_input = VideoFileInput(path)
            if video_input == "webcam":
                self.frame_input = Webcam()
                self.fps = 20
            if video_input == "realsense":
                self.frame_input = Realsense()
                self.fps = 30

            if record_video:
                self.video_logger = VideoLogger(str(int(time.time())), 
                    self.frame_input.get_frame_width(), 
                    self.frame_input.get_frame_height(),
                    self.fps)
                self.video_logger.logging = True
            else:
                self.video_logger = None

            # Select computer vision model
            self.cv_model = Blazepose()

            # Set pose detection method
            self.pose_detection = ComputerVision(queue, cv_model=self.cv_model, 
                frame_input=self.frame_input, hide_video=hide_video,
                record_video=self.video_logger)

        elif input == "vicon":
            self.pose_detection = Vicon(queue)

    def start(self) -> None:
        while self.pose_detection.add_pose_to_queue() and self.cont:
            pass

    def stop(self) -> None:
        self.cont = False
        cv2.destroyAllWindows()
        self.pose_detection.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''
    Generates skeleton data based on arbitrary input. Meant to be consumed
    by the start_ui.py microservice.''')

    parser.add_argument("--queue", choices=["redis", "rabbitmq"], default="redis", help="The type of queue to use to transfer skeleton data.")

    subparsers = parser.add_subparsers(dest="input", description="The input selected to generate skeleton data on.", required=True)

    # Video subparser
    video_parser = subparsers.add_parser('video', description="Generates skeleton data based on video input.")
    video_parser.add_argument("--hide_video", action="store_true", help="Hide real-time video playback.")
    video_parser.add_argument("--record_video", action="store_true", help="Record real-time video playback.")
    video_subparsers = video_parser.add_subparsers(dest="video_input", description="The type of video input to be used.", required=True)
    
    file_parser = video_subparsers.add_parser("file", description="Generate skeleton data based on a video file.")
    file_parser.add_argument("--path", help="Path to the file to be used as the activity", required=True)
    video_subparsers.add_parser("webcam", description="Generate skeleton data based on webcam input.")
    video_subparsers.add_parser("realsense", description="Generate skeleton data based on realsense input.")
    
    # Vicon subparser
    subparsers.add_parser('vicon', description="Generates skeleton data based on vicon input.")
    
    args = parser.parse_args()
    
    pd = PoseService(**vars(args))
    
    try:
        pd.start()
    except KeyboardInterrupt:
        print('Interrupted')
        if pd.video_logger != None:
            print("Stop video logger")
            pd.video_logger.stop_logging()
            pd.video_logger.close()
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

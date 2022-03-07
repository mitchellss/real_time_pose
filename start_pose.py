
import argparse
import os
import sys
from pose_detection.computer_vision.computer_vision import ComputerVision

from pose_detection.computer_vision.cv_model.blazepose import Blazepose
from pose_detection.computer_vision.frame_input.frame_input import FrameInput
from pose_detection.computer_vision.frame_input.realsense import Realsense
from pose_detection.computer_vision.frame_input.video_file_input import VideoFileInput
from pose_detection.computer_vision.frame_input.webcam import Webcam
from pose_detection.pose_detection import PoseDetection
from pose_detection.vicon.vicon import Vicon


class PoseService:

    def __init__(self) -> None:
        self.arg_parse()
        self.pose_detection: PoseDetection = None
        self.frame_input: FrameInput = None

        if self.args.input == "video":
            # Select video input method
            if self.args.video_input == "file":
                self.frame_input = VideoFileInput(self.args.path)
            if self.args.video_input == "webcam":
                self.frame_input = Webcam()
            if self.args.video_input == "realsense":
                self.frame_input = Realsense()

            # Select computer vision model
            self.cv_model = Blazepose()

            # Set pose detection method
            self.pose_detection = ComputerVision(cv_model=self.cv_model, frame_input=self.frame_input, hide_video=self.args.hide_video)

        elif self.args.input == "vicon":
            self.pose_detection = Vicon()

    def start(self) -> None:
        while self.pose_detection.add_pose_to_queue():
            pass

    def arg_parse(self) -> None:
        parser = argparse.ArgumentParser(description='''
            Generates skeleton data based on arbitrary input. Meant to be consumed
            by the start_ui.py microservice.''')

        subparsers = parser.add_subparsers(dest="input", description="The input selected to generate skeleton data on.", required=True)

        # Video subparser
        video_parser = subparsers.add_parser('video', description="Generates skeleton data based on video input.")
        video_parser.add_argument("--hide_video", action="store_true", help="Hide real-time video playback.")
        video_subparsers = video_parser.add_subparsers(dest="video_input", description="The type of video input to be used.", required=True)
        file_parser = video_subparsers.add_parser("file", description="Generate skeleton data based on a video file.")
        file_parser.add_argument("--path", help="Path to the file to be used as the activity", required=True)
        video_subparsers.add_parser("webcam", description="Generate skeleton data based on webcam input.")
        video_subparsers.add_parser("realsense", description="Generate skeleton data based on realsense input.")
        
        # Vicon subparser
        subparsers.add_parser('vicon', description="Generates skeleton data based on vicon input.")
        
        self.args = parser.parse_args()

if __name__ == "__main__":
    pd = PoseService()
    try:
        pd.start()
    except KeyboardInterrupt:
        print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

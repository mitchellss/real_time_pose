
import argparse
import os
import sys
import time
import cv2

from data_logging.logger_factory import LoggerFactory
from frame_input.frame_input_factory import FrameInputFactory
from pose_detection.pose_detection_factory import PoseDetectionFactory
from skeleton_queue.skeleton_queue_factory import SkeletonQueueFactory


class PoseService:
    """
    The pose service program takes some kind of input and produces a pose skeleton. Frame
    input is currently the only kind of input allowed, however there is a dummy class
    that could be used for directly inputting vicon data. Frame data is interpretted by 
    a computer vision model and the resultant skeleton is put in a messaging queue to be
    consumed by the UI service. Experimental Intel Realsense support is being developed
    to allow for real time depth to be incorporated into the model.
    """

    def __init__(self, input:str="video", video_input:str="webcam", path:str=".", 
                 record_video:bool=False, queue_name:str="redis", hide_video:bool=False,
                 cv_model_name:str="blazepose", data_folder_name:str="") -> None:
                
        frame_input_factory = FrameInputFactory(path)
        skeleton_queue_factory = SkeletonQueueFactory()
        pose_detection_factory = PoseDetectionFactory()
        logger_factory = LoggerFactory()

        self.skeleton_queue = skeleton_queue_factory.get_skeleton_queue(queue_name)
        self.pose_detection = pose_detection_factory.get_pose_detection(input, queue_name, cv_model_name)
        
        self.continue_processing = True
        
        if data_folder_name == "":
            self.data_folder_name = str(time.time())
        else:
            self.data_folder_name = data_folder_name

        if input == "video":
            self.video_frame_input, self.fps = frame_input_factory.get_frame_input(video_input)

            if record_video:
                self.video_logger = logger_factory.get_logger("video", data_folder_name=self.data_folder_name, 
                                                              frame_width=self.video_frame_input.get_frame_width(),
                                                              frame_height=self.video_frame_input.get_frame_height(),
                                                              fps=self.fps)
                # VideoLogger(str(int(time.time())), 
                #     self.video_frame_input.get_frame_width(), self.video_frame_input.get_frame_height(),
                #     self.fps)
                self.video_logger.logging = True
            else:
                self.video_logger = None

            self.hide_video = hide_video
            
        elif input == "vicon":
            # vicon specific logic
            pass
        

    def start(self) -> None:
        """Loop infinitely, processing input and adding skeletons to the queue
        until an error occurs or the program is exited.
        """
        while self.continue_processing:
            video_frame = self.video_frame_input.get_video_frame()
            if video_frame is not None:
                preprocessed_frame = cv2.cvtColor(cv2.flip(video_frame, 1), cv2.COLOR_BGR2RGB)
                pose = self.pose_detection.get_skeleton(preprocessed_frame)
                self.skeleton_queue.push_data(pose)
                
                frame_to_log = cv2.cvtColor(preprocessed_frame, cv2.COLOR_RGB2BGR)
                if not self.hide_video:
                    cv2.imshow("MediaPipe Pose", frame_to_log)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break

                if self.video_logger != None:
                    self.video_logger.log(frame_to_log)


    def stop(self) -> None:
        """
        Stop the cv2 window showing the video input and close the video input stream.
        """
        self.continue_processing = False
        cv2.destroyAllWindows()
        self.video_frame_input.close()

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

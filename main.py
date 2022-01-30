import subprocess
import sys
import numpy as np
import argparse
import cv2
from activities.custom_activity.custom_activity import CustomActivity
from activities.custom_activity_dynamic.custom_activity_dynamic import CustomActivityDynamic
from activities.game.game import Game
from activities.game_mk2.game_mk2 import GameMkII
from activities.jumping_jacks.jumping_jacks import JumpingJacks
from activities.squat.squat import Squat
from data_logging.logger import Logger
from data_logging.skeleton_points.point_logger import PointLogger
from data_logging.video.video_logger import VideoLogger
from pyqtgraph import QtCore
from frame_input.realsense import Realsense
from frame_input.video_file_input import VideoFileInput

from frame_input.webcam import Webcam
from pose_detection.blazepose import Blazepose
from ui.pyqtgraph.button_component import ButtonComponent
from ui.pyqtgraph.pyqtgraph import PyQtGraph
from constants.constants import *

class TwoDimensionGame():
    """
    Creates a 2-dimensional user interface displaying the results
    of a pose detection algorithm. Allows users to interact with
    said user interface using detected points on their body.
    """

    NUM_LANDMARKS = 33

    def __init__(self):

        # Ensure correct arguments are passed
        self.arg_parse()

        # Array of the 33 mapped points
        self.body_point_array = np.zeros((self.NUM_LANDMARKS, 2))

        self.pose_detector = Blazepose(model_complexity=1)

        # Initialize realsense or webcam
        if self.args.camera_type == "webcam":
            self.frame_input = Webcam()
        elif self.args.camera_type == "realsense":
            self.frame_input = Realsense()
        elif self.args.camera_type == "video":
            self.frame_input = VideoFileInput(self.args.video_file)

        if not self.args.hide_demo:
            subprocess.Popen(['python', 'play_demo.py', self.args.activity])

        # Init loggers
        self.loggers: list[Logger] = []
        if self.args.record_points:
            self.loggers.append(PointLogger(self.args.activity))
        if self.args.record_video:
            self.loggers.append(VideoLogger(self.args.activity,
                frame_width=self.frame_input.get_frame_width(), 
                frame_height=self.frame_input.get_frame_height()))

    def start(self):
        """Initializes the game's user interface and starts processing data"""
        # Initialize graphs and labels for the user interface
        self.init_ui()

        # Start processing images
        self.start_image_processing()

    def arg_parse(self):
        """Parses the arguments given to the program"""
        parser = argparse.ArgumentParser()
        parser.add_argument("camera_type", choices=["webcam", "realsense", "video"], help="The input type to be used")
        parser.add_argument("--record_points", action="store_true", help="Record point data")
        parser.add_argument("--record_video", action="store_true", help="Record video data")
        parser.add_argument("--activity", nargs="?", const="game", default="game", help="Activity to be recorded, default is game")
        parser.add_argument("--file", nargs="?", const=".", default=".", help="Path to the file to be used as the activity")
        parser.add_argument("--video_file", nargs="?", const=".", default=".", help="Path to video to use as input")
        parser.add_argument("--hide_video", action="store_true", help="Set to hide real-time video playback")
        parser.add_argument("--hide_demo", action="store_true", help="Set to hide demo video")
        self.args = parser.parse_args()

    def init_ui(self):
        """Starts the ui and chooses the correct activity
        to play based on the command line arguments given.
        Registers functional arguments and passes those to
        the relevant activity."""

        # Creates the gui
        self.gui = PyQtGraph()
        self.gui.new_gui()

        # Dict of functions to be given to the activity. This is done this way
        # in order to allow for control of things like logging to be handled by
        # the activity being played rather than by this main file. Moreso, this
        # reduces the amount of coupling between the logger and the activity.
        # Instead of having the activity import the logger and therefore have
        # it be dependant on it, the activity just runs whatever functions are
        # given to it at the times specified in the activity. This allows for
        # very specific activity classes (as intended) but very general logging
        # classes.
        funcs = {
            START_LOGGING:    [logger.start_logging   for logger in self.loggers],
            STOP_LOGGING:     [logger.stop_logging    for logger in self.loggers],
            NEW_LOG:          [logger.new_log         for logger in self.loggers]
        }

        if self.args.activity == "game":
            self.activity = Game(self.body_point_array, funcs=funcs)
        elif self.args.activity == "jumping_jacks":
            self.activity = JumpingJacks(self.body_point_array, funcs=funcs)
        elif self.args.activity == "squat":
            self.activity = Squat(self.body_point_array, funcs=funcs)
        elif self.args.activity == "custom_activity":
            self.activity = CustomActivity(self.body_point_array, funcs=funcs, path=self.args.file)
        elif self.args.activity == "custom_activity_dynamic":
            self.activity = CustomActivityDynamic(self.body_point_array, funcs=funcs, path=self.args.file)
        elif self.args.activity == "game_mk2":
            self.activity = GameMkII(self.body_point_array, funcs=funcs, path=self.args.file)
        else:
            print(f"Cannot find activity: {self.args.activity}")
            sys.exit(1)

        # Dict of components persistant in the ui (don't change between stages)
        # i.e. the clock and the point skeleton components
        self.persistant = self.activity.get_persist()

        # Adds all components to the ui
        for stage in self.activity.get_stages():
            for component in stage:
                self.gui.add_component(stage[component])
                stage[component].hide() # hides all components

        for component in self.persistant:
            self.gui.add_component(self.persistant[component])

        # Call change activity initially to render components
        self.activity.change_stage()

        # Set the function to call on update
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def update(self):
        """
        Updates the position of the skeleton component and
        the time on the timer
        """
        self.persistant[SKELETON].set_pos(self.body_point_array)
        self.persistant[TIMER].tick()

    def start_image_processing(self):
        """
        Infinitely processes new images coming in from the
        frame_input source until the program is exited (esc).
        Passes frames to an object that implements the pose_detection
        interface to get skeleton points. Updates the skeleton, handles
        any kind of activity (i.e. button clicking), and calls the log
        function.
        """
        while True:
            # Get image frame
            color_image = self.frame_input.get_frame()

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(color_image, 1), cv2.COLOR_BGR2RGB)

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            blaze_pose_coords = self.pose_detector.get_pose(image)

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            self.image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # If global coords were successfully found
            if blaze_pose_coords is not None:
                landmarks = blaze_pose_coords.landmark
                self.update_point_and_connection_data(landmarks)

                # Choose to play the default game or a specified activity based on args
                self.handle_activity()

                # log data
                self.log_data()

            if not self.args.hide_video:
                cv2.imshow('MediaPipe Pose', self.image)
            
            #cv2.imshow('Demo', self.d.get_image())
            if cv2.waitKey(5) & 0xFF == 27:
                break

    def update_point_and_connection_data(self, landmarks):
        """Updates the numpy array with the most current coordinate data"""
        # Loop through results and add them to the body point numpy array
        for landmark in range(0,len(landmarks)):
            self.body_point_array[landmark][0] = landmarks[landmark].x
            self.body_point_array[landmark][1] = landmarks[landmark].y

    def handle_activity(self):
        """
        Loops over all the components in the current stage and checks to see if any
        of the specified conditions have been met.
        """
        for component in self.activity.get_components(): # For each component in the dict of active components
            # Handles the logic for buttons
            if isinstance(self.activity.get_components()[component], ButtonComponent):
                # Check to see if each of the target points on the skeleton are touching the button
                for target in self.activity.get_components()[component].target_pts:
                    x: float = self.persistant[SKELETON].skeleton_array[target][0]
                    y: float = self.persistant[SKELETON].skeleton_array[target][1]
                    
                    if self.activity.get_components()[component].is_clicked(x, y, self.activity.get_components()[component].precision):
                        break # Stops rest of for loop from running (caused errors)    

        self.activity.end_frame_reset()        

    def log_data(self):
        """Calls the log method on any instantiated loggers"""
        for logger in self.loggers:
            if isinstance(logger, PointLogger):
                logger.log(self.body_point_array)
            if isinstance(logger, VideoLogger):
                logger.log(self.image)

if __name__ == "__main__":
    td = TwoDimensionGame()
    td.start()
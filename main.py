import pyqtgraph as pg
import mediapipe as mp
import random
import time

import numpy as np
import argparse
import cv2
from pyqtgraph.functions import mkBrush, mkColor
from PyQt5.QtGui import QFont

from frame_input.realsense import Realsense

from frame_input.webcam import Webcam
from pose_detection.blazepose import Blazepose
from ui.pyqtgraph.button_component import ButtonComponent
from ui.pyqtgraph.pyqtgraph import PyQtGraph
from ui.pyqtgraph.skeleton_component import SkeletonComponent
from ui.pyqtgraph.timer_component import TimerComponent


class TwoDimensionGame():

    NUM_LANDMARKS = 33

    def __init__(self):

        # Ensure correct arguments are passed
        self.arg_parse()

        # Initialize starting values for points and labels
        self.init_values()

        # Initialize graphs and labels for the user interface
        self.init_ui()

        # Initialize mediapose stuff
        self.init_mp()

        self.pose_detector = Blazepose()

        # Initialize realsense or webcam
        if self.args.camera_type == "webcam":
            self.frame_input = Webcam()
        elif self.args.camera_type == "realsense":
            self.frame_input = Realsense()

        # Plays video tutorial for activity selected
        # self.play_tutorial()

        # Start processing images
        self.start_image_processing()

    def arg_parse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("camera_type", choices=["webcam", "realsense"], help="The camera type to be used")
        parser.add_argument("--record_points", action="store_true", help="Record point data")
        parser.add_argument("--record_video", action="store_true", help="Record video data")
        parser.add_argument("--activity", nargs="?", const="game", default="game", help="Activity to be recorded, default is game")
        self.args = parser.parse_args()

    def init_values(self):
        self.score = 0
        self.countdown_time = 0

        # Array of the 33 mapped points
        self.body_point_array = np.zeros((self.NUM_LANDMARKS, 2))

        # Coordinates for the targets for the user to pop
        self.target_1_x = 0
        self.target_1_y = 0
        self.target_2_x = 0
        self.target_2_y = 0

        # Coordinates for start target
        self.start_target_x = 0
        self.start_target_y = -1

        # Game State:
        # 0 - Start screen
        # 1 - Active game
        # 2 - Name input
        self.game_state = 0

        self.name_input_1_index = 0
        self.name_input_2_index = 0
        self.name_input_3_index = 0

        self.submit_name_x = 0.7
        self.submit_name_y = 0

        self.time_btw_letter_change = 0

        self.vid_playing = False

    def init_ui(self):

        # Creates the gui
        self.gui = PyQtGraph()
        self.gui.new_gui()

        # Parses activity yaml file and adds components to the ui
        self.components = self.parse_activity_ui_yaml()

        # Adds components to the gui
        for component in self.components:
            self.gui.add_component(self.components[component])

        # Set the function to call on update
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def parse_activity_ui_yaml(self):
        components = {}
        
        # TODO: Parse through activity yaml to create these components

        components["start_button"] = ButtonComponent(50, pg.mkBrush(0, 255, 0, 120), self.start_target_x, self.start_target_y, func=self.start_button_func)
        components["target_1"] = ButtonComponent(50, pg.mkBrush(255, 0, 0, 120), self.target_1_x, self.target_1_y, func=self.target_1_func)
        components["target_2"] = ButtonComponent(50, pg.mkBrush(0, 0, 255, 120), self.target_2_x, self.target_2_y, func=self.target_2_func)
        components["skeleton"] = SkeletonComponent(self.body_point_array)
        components["timer"] = TimerComponent(0.4, -1.2, font=QFont("Arial", 30), text="Time: ", starting_time=10)

        return components

    def update(self):
        self.components["skeleton"].set_pos(self.body_point_array)
        self.components["timer"].tick()
        

    def init_mp(self):
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_drawing = mp.solutions.drawing_utils

    def start_image_processing(self):
        while True:
            # Get image frame
            color_image = self.frame_input.get_frame()

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(color_image, 1), cv2.COLOR_BGR2RGB)

            # Record video if flag is set
            if self.args.record_video:
                if self.game_state == 1:
                    self.vid_writer.write(color_image)

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            blaze_pose_coords = self.pose_detector.get_pose(image)

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # If global coords were successfully found
            if blaze_pose_coords is not None:
                landmarks = blaze_pose_coords.landmark
                self.update_point_and_connection_data(blaze_pose_coords, landmarks)

                # Choose to play the default game or a specified activity based on args
                self.handle_activity()

                # Record data points if flag is set
                if self.args.record_points:
                    self.log_data()
                
            cv2.imshow('MediaPipe Pose', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    def log_data(self):
        if self.components["timer"].get_time() > 0:
            self.point_data_file.write(str(time.time()) + "," + ','.join([f"{num[0]},{num[1]}" for num in self.body_point_array]) + "\n")
            
    def handle_activity(self):
        self.components["start_button"].is_clicked(self.components["skeleton"].skeleton_array[self.components["skeleton"].LEFT_HAND][0], 
            self.components["skeleton"].skeleton_array[self.components["skeleton"].LEFT_HAND][1], 0.1)
        
        if self.components["timer"].get_time() > 0:
            self.components["target_1"].is_clicked(self.components["skeleton"].skeleton_array[self.components["skeleton"].RIGHT_HAND][0], 
                self.components["skeleton"].skeleton_array[self.components["skeleton"].RIGHT_HAND][1], 0.1)
            self.components["target_2"].is_clicked(self.components["skeleton"].skeleton_array[self.components["skeleton"].LEFT_HAND][0], 
                self.components["skeleton"].skeleton_array[self.components["skeleton"].LEFT_HAND][1], 0.1)

    def target_1_func(self):
        self.components["target_1"].set_pos(random.uniform(-0.7,0.7), random.uniform(0.0,-0.8))
        self.score += 1

    def target_2_func(self):
        self.components["target_2"].set_pos(random.uniform(-0.7,0.7), random.uniform(0.0,-0.8))
        self.score += 1

    def start_button_func(self):
        self.countdown_time = 10
        self.components["start_button"].hide()

    def update_point_and_connection_data(self, blaze_pose_coords, landmarks):
        # Loop through results and add them to the body point numpy array
        for landmark in range(0,len(landmarks)):
            self.body_point_array[landmark][0] = landmarks[landmark].x
            self.body_point_array[landmark][1] = landmarks[landmark].y

if __name__ == "__main__":
    td = TwoDimensionGame()
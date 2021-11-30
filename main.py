import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtGui import QFont
import mediapipe as mp
import random
#from time import time 
import time
import os

import numpy as np
import argparse, sys
import cv2
from pyqtgraph.functions import mkBrush, mkColor

import subprocess

class TwoDimensionGame():

    NUM_LANDMARKS = 33
    NUM_CONNECTIONS = 35
    RED_LANDMARK = 15
    BLUE_LANDMARK = 16

    # Where to connect limbs. Refer to here 
    # https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png
    CONNECTIONS = np.array([
        [16,14], [16,18], [16,20], [16,22],
        [18,20], [14,12], [12,11], [12,24],
        [11,23], [11,13], [15,13], [15,17],
        [15,19], [15,21], [17,19], [24,23],
        [26,24], [26,28], [25,23], [25,27],
        [10,9], [8,6], [5,6], [5,4], [0,4],
        [0,1], [2,1], [2,3], [3,7], [28,32],
        [28,30], [27,29], [27,31], [32,30],
        [29,31]
    ])

    LETTER_SELECT = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N',
                        'O','P','Q','R','S','T','U','V','W','X','Y','Z']

    def __init__(self):

        # Ensure correct arguments are passed
        self.arg_parse()

        # Initialize starting values for points and labels
        self.init_values()

        # Initialize graphs and labels for the user interface
        self.init_ui()

        # Initialize mediapose stuff
        self.init_mp()

        # Initialize realsense or webcam
        self.init_camera()

        self.play_tutorial()

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

        # Coordinates for name change labels
        self.name_input_label_1_x = -0.25
        self.name_input_label_1_y = -1.25
        self.name_input_label_2_x = 0
        self.name_input_label_2_y = -1.25
        self.name_input_label_3_x = 0.25
        self.name_input_label_3_y = -1.25

        # Coordinates for name change targets
        self.name_input_1_x = -0.25
        self.name_input_1_y = -1
        self.name_input_2_x = 0
        self.name_input_2_y = -1
        self.name_input_3_x = 0.25
        self.name_input_3_y = -1

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
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('2D Game')

        # Create plot and set range
        self.plot = self.win.addPlot()
        self.plot.setXRange(-1, 1)
        self.plot.setYRange(-1.2, 0.8)
        self.plot.getViewBox().invertY(True)

        # Create scatter and targets
        self.scatter = pg.GraphItem()
        self.start_target = pg.ScatterPlotItem(size=50, brush=pg.mkBrush(0, 255, 0, 120))

        # Time label
        self.countdown_text = pg.TextItem(text=f"Time: {self.countdown_time}s")
        self.countdown_text.setPos(0.4,-1.2)
        self.countdown_text.setFont(QFont('Arial', 30))

        if (self.args.activity == "game"):
            self.target_1 = pg.ScatterPlotItem(size=50, brush=pg.mkBrush(255, 0, 0, 120)) 
            self.target_2 = pg.ScatterPlotItem(size=50, brush=pg.mkBrush(0, 0, 255, 120)) 
            self.name_input = pg.ScatterPlotItem(size=50, brush=pg.mkBrush(255, 255, 255, 120))
            self.name_submit_scatter = pg.ScatterPlotItem(size=50, brush=pg.mkBrush(0, 255, 0, 120))
            self.left_hand_color_scatter = pg.ScatterPlotItem(size=50, brush=pg.mkBrush(255,0,0,120))
            self.right_hand_color_scatter = pg.ScatterPlotItem(size=50, brush=pg.mkBrush(0,0,255,120))

            # Score label
            self.score_text = pg.TextItem(text=f"Score: {self.score}")
            self.score_text.setPos(0.4,-1)
            self.score_text.setFont(QFont('Arial', 30))


            # Submit name label
            self.name_submit = pg.TextItem(text="Submit")
            self.name_submit.setPos(0.6,-0.3)
            self.name_submit.setFont(QFont('Arial', 20))

            # Name input labels
            self.name_input_1 = pg.TextItem(text=f"{self.LETTER_SELECT[self.name_input_1_index]}")
            self.name_input_2 = pg.TextItem(text=f"{self.LETTER_SELECT[self.name_input_2_index]}")
            self.name_input_3 = pg.TextItem(text=f"{self.LETTER_SELECT[self.name_input_3_index]}")
            self.name_input_1.setPos(self.name_input_label_1_x, self.name_input_label_1_y)
            self.name_input_2.setPos(self.name_input_label_2_x, self.name_input_label_2_y)
            self.name_input_3.setPos(self.name_input_label_3_x, self.name_input_label_3_y)
            self.name_input_1.setFont(QFont('Arial', 30))
            self.name_input_2.setFont(QFont('Arial', 30))
            self.name_input_3.setFont(QFont('Arial', 30))
            self.target_1.setData(pos=[[self.target_1_x, self.target_1_y]])
            self.target_2.setData(pos=[[self.target_2_x, self.target_2_y]])
            self.name_input.setData(pos=[[self.name_input_1_x,self.name_input_1_y], 
                                            [self.name_input_2_x,self.name_input_2_y], 
                                            [self.name_input_3_x,self.name_input_3_y]])
            self.name_submit_scatter.setData(pos=[[self.submit_name_x,self.submit_name_y]])
            self.left_hand_color_scatter.setData(pos=[[0,0]])
            self.right_hand_color_scatter.setData(pos=[[0,0]])
            self.plot.addItem(self.score_text)
            self.plot.addItem(self.target_1)
            self.plot.addItem(self.target_2)
            self.plot.addItem(self.name_input)
            self.plot.addItem(self.name_input_1)
            self.plot.addItem(self.name_input_2)
            self.plot.addItem(self.name_input_3)
            self.plot.addItem(self.name_submit)
            self.plot.addItem(self.name_submit_scatter)
            self.plot.addItem(self.left_hand_color_scatter)
            self.plot.addItem(self.right_hand_color_scatter)
            # Hide targets
            self.target_1.hide()
            self.target_2.hide()

            # Hide name inputs
            self.name_input_1.hide()
            self.name_input_2.hide()
            self.name_input_3.hide()
            self.name_input.hide()

            # Hide submit name
            self.name_submit.hide()
            self.name_submit_scatter.hide()

        # Set data for scatter and targets
        self.scatter.setData(pos=self.body_point_array, 
                            adj=self.CONNECTIONS, 
                            pen=pg.mkPen(mkColor(255,255,255,120),width=2),
                            symbolBrush=mkBrush(255,255,255,120),
                            symbolPen=None)
        self.start_target.setData(pos=[[self.start_target_x, self.start_target_y]])

        # Add items to the plot
        self.plot.addItem(self.scatter)
        self.plot.addItem(self.start_target)
        self.plot.addItem(self.countdown_text)


        # Set the function to call on update
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def update(self):
        self.scatter.setData(pos=self.body_point_array)

        if (self.args.activity == "game"):
            self.target_1.setData(pos=[[self.target_1_x,self.target_1_y]])
            self.target_2.setData(pos=[[self.target_2_x,self.target_2_y]])

        if (self.game_state == 1 and self.countdown_time > 0):# and not self.vid_playing):
            self.countdown_time -= 0.05
        else:
            self.countdown_time = 0

        if (self.countdown_time == 0):
            self.time_btw_letter_change += 0.05
        
        self.countdown_text.setText(text=f"Time: {round(self.countdown_time,1)}")
        if (self.args.activity == "game"):
            self.score_text.setText(text=f"Score: {self.score}")
            self.left_hand_color_scatter.setData(pos=[self.body_point_array[15]])
            self.right_hand_color_scatter.setData(pos=[self.body_point_array[16]])

    def init_mp(self):
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

    def init_camera(self):
        if self.args.camera_type == "realsense":
            self.pipeline = self.config_realsense()
        elif self.args.camera_type == "webcam":
            self.cap = cv2.VideoCapture(0)
            self.vid_width= int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.vid_height= int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def config_realsense(self):
        # Configure depth and color streams 
        import pyrealsense2 as rs
        pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        # Tries to find the rgb camera
        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        if device_product_line == 'L500':
            config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        # Start streaming
        pipeline.start(config)

        return pipeline

    def start_image_processing(self):
        # Model complexity:
        # 0 : Light
        # 1 : Full
        # 2 : Heavy
        with self.mp_pose.Pose(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
                model_complexity=1) as pose:

            while True:
                # Get realsense color image
                if self.args.camera_type == "realsense":
                    color_image = self.get_realsense_image()
                    if color_image is None:
                        continue

                # Get webcam color image
                elif self.args.camera_type == "webcam":
                    success, color_image = self.cap.read()


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
                results = pose.process(image)

                # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Draws joints and limbs on video
                self.mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())

                # Gets pose coordinates from the image processing results
                blaze_pose_coords = results.pose_world_landmarks

                # If global coords were successfully found
                if blaze_pose_coords is not None:
                    landmarks = blaze_pose_coords.landmark
                    self.update_point_and_connection_data(blaze_pose_coords, landmarks)

                    # Choose to play the default game or a specified activity based on args
                    if self.args.activity == "game":
                        self.handle_game()
                    else:
                        self.handle_activity()

                    # Record data points if flag is set
                    if self.args.record_points:
                        self.log_data()

                cv2.imshow('MediaPipe Pose', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break

    def log_data(self):
        if self.countdown_time > 0:
            self.point_data_file.write(str(time.time()) + "," + ','.join([f"{num[0]},{num[1]}" for num in self.body_point_array]) + "\n")
            
    def handle_game(self):

        if self.countdown_time > 0:
            dist_from_pt1 = self.get_distance_between_pts(self.body_point_array[self.RED_LANDMARK][0],
                                                            self.body_point_array[self.RED_LANDMARK][1],
                                                            self.target_1_x, self.target_1_y)

            dist_from_pt2 = self.get_distance_between_pts(self.body_point_array[self.BLUE_LANDMARK][0],
                                                            self.body_point_array[self.BLUE_LANDMARK][1],
                                                            self.target_2_x, self.target_2_y)
            if dist_from_pt1 < 0.1:
                self.target_1_x = random.uniform(-0.7,0.7)
                self.target_1_y = random.uniform(0.0,-0.8)
                #s.send(msg)
                self.score += 1

            if dist_from_pt2 < 0.1:
                self.target_2_x = random.uniform(-0.7,0.7)
                self.target_2_y = random.uniform(0.0,-0.8)
                #s.send(msg2)
                self.score += 1
        else:
            if self.game_state == 0:
                self.handle_start_screen()

            elif self.game_state == 1:
                self.handle_name_input()

    def handle_start_screen(self):
        # Start screen
        self.start_target.show()
        if (self.args.activity == "game"):
            self.target_1.hide()
            self.target_2.hide()

        if self.get_distance_between_pts(self.body_point_array[15][0],
                                                self.body_point_array[15][1],
                                                self.start_target_x, self.start_target_y) < 0.2 \
                                                or \
                                                self.get_distance_between_pts(self.body_point_array[16][0],
                                                self.body_point_array[16][1],
                                                self.start_target_x, self.start_target_y) < 0.2:
            self.start_target.hide()
            if (self.args.activity == "game"):
                self.target_1.show()
                self.target_2.show()
            self.game_state = 1
            self.score = 0
            current_time = int(time.time())

            if self.args.record_points or self.args.record_video:
                os.mkdir(f"./data/{current_time}_{self.args.activity}")

            if self.args.record_points:
                self.point_data_file = open(f"./data/{current_time}_{self.args.activity}/{self.args.activity}_point_data.csv", "a")
                self.point_data_file.write("timestamp,x00,y00,x01,y01,x02,y02,x03,y03,x04,y04,x05,y05,x06,y06,x07,y07,x08,y08,x09,y09,x10,y10,x11,y11,x12,y12,x13,y13,x14,y14,x15,y15,x16,y16,x17,y17,x18,y18,x19,y19,x20,y20,x21,y21,x22,y22,x23,y23,x24,y24,x25,y25,x26,y26,x27,y27,x28,y28,x29,y29,x30,y30,x31,y31,x32,y32\n")
                    
            if self.args.record_video:
                self.vid_writer = cv2.VideoWriter(f'./data/{current_time}_{self.args.activity}/{self.args.activity}.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (self.vid_width,self.vid_height))

            if self.args.activity != "game":
                self.game_state = 1
                #time.sleep(5)
            
            self.countdown_time = 10

    def handle_name_input(self):
        self.target_1.hide()
        self.target_2.hide()
        self.name_input_1.show()
        self.name_input_2.show()
        self.name_input_3.show()
        self.name_input.show()
        #self.score_text.hide()
        self.countdown_text.hide()
        self.name_submit_scatter.show()
        self.name_submit.show()
        if self.args.record_points:
            self.point_data_file.close()
        if self.args.record_video:
            self.vid_writer.release()

        # Check if name input 1 clicked
        if self.time_btw_letter_change > 0.2 and (self.get_distance_between_pts(self.body_point_array[15][0],
                self.body_point_array[15][1],
                self.name_input_1_x, self.name_input_1_y) < 0.2 \
                or \
                self.get_distance_between_pts(self.body_point_array[16][0],
                self.body_point_array[16][1],
                self.name_input_1_x, self.name_input_1_y) < 0.2):
            self.name_input_1_index += 1
            self.name_input_1.setText(f"{self.LETTER_SELECT[self.name_input_1_index % len(self.LETTER_SELECT)]}")
            self.time_btw_letter_change = 0

                # Check if name input 2 clicked
        if self.time_btw_letter_change > 0.2 and (self.get_distance_between_pts(self.body_point_array[15][0],
                                self.body_point_array[15][1],
                                self.name_input_2_x, self.name_input_2_y) < 0.2 \
                                or \
                                self.get_distance_between_pts(self.body_point_array[16][0],
                                self.body_point_array[16][1],
                                self.name_input_2_x, self.name_input_2_y) < 0.2):
            self.name_input_2_index += 1
            self.name_input_2.setText(f"{self.LETTER_SELECT[self.name_input_2_index % len(self.LETTER_SELECT)]}")
            self.time_btw_letter_change = 0

                # Check if name input 3 clicked
        if self.time_btw_letter_change > 0.2 and (self.get_distance_between_pts(self.body_point_array[15][0],
                                self.body_point_array[15][1],
                                self.name_input_3_x, self.name_input_3_y) < 0.2 \
                                or \
                                self.get_distance_between_pts(self.body_point_array[16][0],
                                self.body_point_array[16][1],
                                self.name_input_3_x, self.name_input_3_y) < 0.2):
            self.name_input_3_index += 1
            self.name_input_3.setText(f"{self.LETTER_SELECT[self.name_input_3_index % len(self.LETTER_SELECT)]}")
            self.time_btw_letter_change = 0

                # Check if submit button clicked
        if self.get_distance_between_pts(self.body_point_array[15][0],
                                self.body_point_array[15][1],
                                self.submit_name_x, self.submit_name_y) < 0.2 \
                                or \
                                self.get_distance_between_pts(self.body_point_array[16][0],
                                self.body_point_array[16][1],
                                self.submit_name_x, self.submit_name_y) < 0.2:
            self.name_input_1.hide()
            self.name_input_2.hide()
            self.name_input_3.hide()
            self.name_input.hide()
            self.countdown_text.show()
            self.name_submit_scatter.hide()
            self.name_submit.hide()
            self.start_target.show()
            self.game_state = 0
            self.submit_score()

    def handle_activity(self):
        if self.countdown_time > 0:
            True
        else:
            if self.game_state == 0:
                self.handle_start_screen()
            else:
                print("done video")
                if self.args.record_points:
                    self.point_data_file.close()
                if self.args.record_video:
                    self.vid_writer.release()
                
                self.game_state = 0

    def play_tutorial(self):
        subprocess.Popen(['python', 'test.py', self.args.activity])

    def get_distance_between_pts(self, x1, y1, x2, y2):
        return abs((x1 - x2)**2 + (y1 - y2)**2)**0.5

    def submit_score(self):
        file = open("leaderboard.txt", "a")
        file.write(f"{self.LETTER_SELECT[self.name_input_1_index % len(self.LETTER_SELECT)]}{self.LETTER_SELECT[self.name_input_2_index % len(self.LETTER_SELECT)]}{self.LETTER_SELECT[self.name_input_3_index % len(self.LETTER_SELECT)]},{self.score}\n")
        file.close()

        with open('leaderboard.txt') as f:
            lines = f.read().splitlines()
            for i in range(0,len(lines)):
                lines[i] = lines[i].split(",")

            def myFunc(e):
                return int(e[1])
            
            lines.sort(key=myFunc, reverse=True)

            self.print_scoreboard(lines)
    
    def print_scoreboard(self, lines):
        print("\n" * 50)
        for i in range(0,10):
            try:
                print(f"{i+1}. {lines[i][0]} - {lines[i][1]}")
            except:
                continue

    def update_point_and_connection_data(self, blaze_pose_coords, landmarks):
        # Loop through results and add them to the body point numpy array
        for landmark in range(0,len(landmarks)):
            self.body_point_array[landmark][0] = landmarks[landmark].x
            self.body_point_array[landmark][1] = landmarks[landmark].y

    def get_realsense_image(self):
        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            return None

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        return color_image


if __name__ == "__main__":
    import sys

    td = TwoDimensionGame()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
import cv2
import mediapipe as mp
import numpy as np
import random

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

_PRESENCE_THRESHOLD = 0.5
_VISIBILITY_THRESHOLD = 0.5
_RGB_CHANNELS = 3
WHITE_COLOR = (224, 224, 224)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 128, 0)
BLUE_COLOR = (255, 0, 0)
NUM_LANDMARKS = 33
NUM_CONNECTIONS = 35

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('Python Step Counter')

# Create two plots, one for raw data and
# the other for data after filters, etc.
plot1 = win.addPlot()

# Set X and Y limits on graph
plot1.setXRange(-1, 1)
plot1.setYRange(-1, 1)

plot1.getViewBox().invertY(True)

# Array of the 33 mapped points
body_point_array = np.zeros((NUM_LANDMARKS, 2))

# Array of the 35 connections (2 points for each connection)
limb_array = np.ndarray((NUM_CONNECTIONS*2 + 4, 2))

scatter = pg.ScatterPlotItem(size=10, brush=pg.mkBrush(255, 255, 255, 120)) 

point1 = pg.ScatterPlotItem(size=50, brush=pg.mkBrush(255, 0, 0, 120)) 
point2 = pg.ScatterPlotItem(size=50, brush=pg.mkBrush(0, 0, 255, 120)) 

scatter1 = plot1.addItem(scatter)
point11 = plot1.addItem(point1)
point22 = plot1.addItem(point2)
#curve1 = plot1.plot([1,2,3,4], [1,2,3,4])

scatter.setData(pos=body_point_array)

point1_x = 0
point1_y = 0

point2_x = 0
point2_y = 0
point1.setData(pos=[[point1_x, point1_y]])
point2.setData(pos=[[point2_x, point2_y]])

def update():
    scatter.setData(pos=body_point_array)
    point1.setData(pos=[[point1_x,point1_y]])
    point2.setData(pos=[[point2_x,point2_y]])


t = QtCore.QTimer()
t.timeout.connect(update)
t.start(50)

mp_drawing_styles = mp.solutions.drawing_styles
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

try:
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
except:
    cap = cv2.VideoCapture(0)

def _normalize_color(color):
    return tuple(v / 255. for v in color)

def angle(v1, v2, acute):
    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    if (acute == True):
        return angle
    else:
        return 2 * np.pi - angle

# Model complexity:
# 0 : Light
# 1 : Full
# 2 : Heavy
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=1) as pose:
    while True:
        
        try:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
        except:
            success, color_image = cap.read()
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(color_image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draws joints and limbs on video
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        # Gets pose coordinates from the image processing results
        blaze_pose_coords = results.pose_world_landmarks

        # Dictionary of where to connect limbs. Refer to here 
        # https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png
        connection_dict = {
            16:[14, 18, 20, 22],
            18:[20],
            14:[12],
            12:[11, 24],
            11:[23, 13],
            15:[13, 17, 19, 21],
            17:[19],
            24:[23],
            26:[24,28],
            25:[23,27],
            10:[9],
            8:[6],
            5:[6,4],
            0:[4,1],
            2:[1,3],
            3:[7],
            28:[32,30],
            27:[29, 31],
            32:[30],
            29:[31]
        }

        # If global coords were successfully found
        if blaze_pose_coords is not None:
            landmarks = blaze_pose_coords.landmark

            # Loop through results and add them to the body point numpy array
            for landmark in range(0,len(landmarks)):
                body_point_array[landmark][0] = landmarks[landmark].x
                body_point_array[landmark][1] = landmarks[landmark].y
                #body_point_array[landmark][2] = landmarks[landmark].z

            # Add limb coordinates to limb numpy array
            index = 0
            for connection_index in range(0, 35):
                if connection_index in connection_dict:
                    for connection in range(0, len(connection_dict[connection_index])):

                        limb_array[index][0] = blaze_pose_coords.landmark[connection_index].x
                        limb_array[index][1] = blaze_pose_coords.landmark[connection_index].y
                        #limb_array[index][2] = blaze_pose_coords.landmark[connection_index].z

                        limb_array[index + 1][0] = blaze_pose_coords.landmark[connection_dict[connection_index][connection]].x
                        limb_array[index + 1][1] = blaze_pose_coords.landmark[connection_dict[connection_index][connection]].y
                        #limb_array[index + 1][2] = blaze_pose_coords.landmark[connection_dict[connection_index][connection]].z

                        index += 2

            left_arm = body_point_array[11] - body_point_array[13] # technically the model's right arm but image is flipped
            left_forearm = body_point_array[15] - body_point_array[13] 

            right_arm = body_point_array[12] - body_point_array[14] # technically the model's left arm but image is flipped
            right_forearm = body_point_array[16] - body_point_array[14] 

            dist_from_pt1 = ((body_point_array[15][0] - point1_x)**2 + (body_point_array[15][1] - point1_y)**2)**0.5
            dist_from_pt2 = ((body_point_array[16][0] - point2_x)**2 + (body_point_array[16][1] - point2_y)**2)**0.5
            if dist_from_pt1 < 0.1:
                point1_x = random.uniform(-0.7,0.7)
                point1_y = random.uniform(0.0,-0.8)
            if dist_from_pt2 < 0.2:
                point2_x = random.uniform(-0.7,0.7)
                point2_y = random.uniform(0.0,-0.8)

            #print(f"Right arm angle: {round(180*angle(left_arm,left_forearm,True)/np.pi,2)} \
            #Left arm angle: {round(180*angle(right_arm,right_forearm,True)/np.pi,2)}", end="\r")

        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

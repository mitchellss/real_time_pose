import cv2
import mediapipe as mp
import numpy as np
import pyrealsense2 as rs
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui
import sys, argparse

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

# Dictionary of where to connect limbs. Refer to here 
# https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png
CONNECTION_DICT = {
    16:[14, 18, 20, 22], 18:[20], 14:[12],
    12:[11, 24], 11:[23, 13], 15:[13, 17, 19, 21],
    17:[19], 24:[23], 26:[24,28], 25:[23,27],
    10:[9], 8:[6], 5:[6,4], 0:[4,1], 2:[1,3],
    3:[7], 28:[32,30], 27:[29, 31], 32:[30], 29:[31]
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("camera_type", choices=["webcam", "realsense"], help="The camera type to be used")
    args = parser.parse_args()

    app = QtGui.QApplication([])
    w = gl.GLViewWidget()
    w.show()

    # Array of the 33 mapped points
    body_point_array = np.ndarray((NUM_LANDMARKS, 3))

    # Array of the 35 connections (2 points for each connection)
    limb_array = np.ndarray((NUM_CONNECTIONS*2 + 4, 3))

    # Create the background grid
    gz = gl.GLGridItem()
    gz.translate(0, 0, -1)
    w.addItem(gz)

    # Create 3D scatter plot for joints
    joint_scatter_plot = gl.GLScatterPlotItem(pos=body_point_array)
    joint_scatter_plot.rotate(90, -1, 0, 0) # Rotate to upright position

    # Create 3D line plot for limbs
    limb_line_plot = gl.GLLinePlotItem(pos=limb_array, mode="lines", width=2.0)
    limb_line_plot.rotate(90, -1, 0, 0) # Rotate to upright position

    # Add 3D scatter plot and line plot to pyqtgraph
    w.addItem(joint_scatter_plot)
    w.addItem(limb_line_plot)

    def update():
        joint_scatter_plot.setData()
        limb_line_plot.setData()

    t = QtCore.QTimer()
    t.timeout.connect(update)
    t.start(50)

    mp_drawing_styles = mp.solutions.drawing_styles
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    if args.camera_type == "realsense":
        # Configure depth and color streams 
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
    elif args.camera_type == "webcam":
        pass

    # Model complexity:
    # 0 : Light
    # 1 : Full
    # 2 : Heavy
    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=2) as pose:

        while True:
            if args.camera_type == "realsense":
                # Wait for a coherent pair of frames: depth and color
                frames = pipeline.wait_for_frames()
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()
                if not depth_frame or not color_frame:
                    continue

                # Convert images to numpy arrays
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())
            elif args.camera_type == "webcam":
                # TODO: webcam implementation
                pass

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
            blaze_pose_global_coords = results.pose_world_landmarks

            # If global coords were successfully found
            if blaze_pose_global_coords is not None:
                landmarks = blaze_pose_global_coords.landmark

                # Loop through results and add them to the body point numpy array
                for landmark in range(0,len(landmarks)):
                    populate_body_point_array(body_point_array, landmarks, landmark)

                # Add limb coordinates to limb numpy array
                index = 0
                for connection_index in range(0, 35):
                    if connection_index in CONNECTION_DICT:
                        for connection in range(0, len(CONNECTION_DICT[connection_index])):
                            populate_limb_array(limb_array, blaze_pose_global_coords, index, connection_index, connection)
                            index += 2

                # technically the model's left arm but image is flipped
                right_arm_angle = get_three_point_angle(11, 13, 15, body_point_array)

                # technically the model's right arm but image is flipped
                left_arm_angle = get_three_point_angle(12, 14, 16, body_point_array)

                print(f"Right arm angle: {right_arm_angle} \
                Left arm angle: {left_arm_angle}", end="\r")

            cv2.imshow('MediaPipe Pose', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

            def _normalize_color(color):
                return tuple(v / 255. for v in color)


def populate_body_point_array(body_point_array, landmarks, landmark):
    body_point_array[landmark][0] = landmarks[landmark].x
    body_point_array[landmark][1] = landmarks[landmark].y
    body_point_array[landmark][2] = landmarks[landmark].z

def populate_limb_array(limb_array, blaze_pose_global_coords, index, connection_index, connection):
    limb_array[index][0] = blaze_pose_global_coords.landmark[connection_index].x
    limb_array[index][1] = blaze_pose_global_coords.landmark[connection_index].y
    limb_array[index][2] = blaze_pose_global_coords.landmark[connection_index].z

    limb_array[index + 1][0] = blaze_pose_global_coords.landmark[CONNECTION_DICT[connection_index][connection]].x
    limb_array[index + 1][1] = blaze_pose_global_coords.landmark[CONNECTION_DICT[connection_index][connection]].y
    limb_array[index + 1][2] = blaze_pose_global_coords.landmark[CONNECTION_DICT[connection_index][connection]].z

def get_three_point_angle(landmark_1, middle_landmark, landmark_2, body_point_array):
    limb_1 = body_point_array[landmark_1] - body_point_array[middle_landmark] 
    limb_2 = body_point_array[landmark_2] - body_point_array[middle_landmark] 
    return round(180*angle(limb_1, limb_2, True)/np.pi,2)

def angle(v1, v2, acute):
    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    if (acute):
        return angle
    else:
        return 2 * np.pi - angle

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':

    main()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

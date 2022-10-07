"""
Example program that shows a basic usage of the library.
A button and skeleton component are added to a scene that
takes input from a webcam and gets pose data from Google's
Blazepose
"""
import realtimepose as rtp

# Specify input as a webcam and computer vision model as blazepose
frame_input: rtp.FrameInput = rtp.Webcam(device_num=0, fps=30)
cv_model: rtp.CVModel = rtp.BlazePose()

# Create a pose generator based on a webcam + blazepose
pose_input: rtp.PoseGenerator = rtp.ComputerVisionPose(
    frame_input=frame_input, model=cv_model)

# Specify GUI to be pygame
ui: rtp.UserInterface = rtp.PyGameUI(width=1920//2, height=1080//2, fps=60)

# Create activity
activity = rtp.Activity(pose_input=pose_input, frontend=ui)

# Create a new scene
scene_1 = rtp.Scene()
activity.add_scene(scene_1)

# Create a button that prints "Hello world!" when clicked
button_1: rtp.Button = rtp.button(
    gui=ui, x_coord=1920//2, y_coord=1080//2, 
    targets=[cv_model.LEFT_HAND, cv_model.RIGHT_HAND], 
    activation_distance=50, callback=lambda: print("Hello world!"))

# Create a skeleton to map pose points to
skeleton: rtp.Skeleton = rtp.skeleton(gui=ui, x_coord=200, y_coord=200)

# Add the skeleton and button to the scene  
scene_1.add_component(button_1)
scene_1.add_component(skeleton)

# Start activity
activity.run()

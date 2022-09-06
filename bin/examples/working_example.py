"""
Example program that shows a basic usage of the library.
A button and skeleton component are added to a scene that
takes input from a webcam and gets pose data from Google's
Blazepose
"""
import realtimepose as rtp

# Specify input
webcam: rtp.FrameInput = rtp.Webcam(device_num=0, fps=30)
blazepose: rtp.CVModel = rtp.BlazePose()
webcam_pose: rtp.PoseGenerator = rtp.ComputerVisionPose(
    frame_input=webcam, model=blazepose)

# Specify GUI
ui: rtp.UserInterface = rtp.PyGameUI(width=1920//2, height=1080//2, fps=60)

# Create activity
activity = rtp.Activity(pose_input=webcam_pose, frontend=ui)

# Add components to scene
scene_1 = rtp.Scene()
button_1: rtp.Button = rtp.button(gui=ui, x_coord=1920//2, y_coord=1080//2)
skeleton: rtp.Skeleton = rtp.skeleton(gui=ui, x_coord=200, y_coord=200)
scene_1.add_component(button_1)
scene_1.add_component(skeleton)

# Add scene to activity
activity.add_scene(scene_1)

# Start
activity.run()
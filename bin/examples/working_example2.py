"""Test"""
import realtimepose2 as rtp
from realtimepose2.core.displaying.components import button


def callback_func():
    """Test"""
    print("Hello world!")


# Specify input
webcam: rtp.FrameInput = rtp.Webcam()
blazepose: rtp.CVModel = rtp.BlazePose()
webcam_pose: rtp.PoseGenerator = rtp.ComputerVisionPose(
    frame_input=webcam, model=blazepose)

# Specify GUI
ui: rtp.UserInterface = rtp.PyGameUI()
# ui: rtp.UserInterface = rtp.Pyglet()

# Create activity
activity = rtp.Activity(pose_input=webcam_pose, frontend=ui)

# Add scene to activity
scene_1 = rtp.Scene()

button_1: rtp.Button = button(gui=ui, x_coord=0.0, y_coord=0.0)

scene_1.add_component(button_1)

# print(button_1.is_clicked(0, 0, 5))
# print(button_1.render())

activity.add_scene(scene_1)

# Start
activity.run()

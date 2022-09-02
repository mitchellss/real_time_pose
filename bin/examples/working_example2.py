"""Test"""
import realtimepose2 as rtp


def callback_func():
    """Test"""
    print("Hello world!")


# Specify input
webcam: rtp.FrameInput = rtp.Webcam(device_num=0)
blazepose: rtp.CVModel = rtp.BlazePose()
webcam_pose: rtp.PoseGenerator = rtp.ComputerVisionPose(
    frame_input=webcam, model=blazepose)

# Specify GUI
ui: rtp.UserInterface = rtp.PyGameUI(width=1920, height=1080, fps=60)

# Create activity
activity = rtp.Activity(pose_input=webcam_pose, frontend=ui)

# Add scene to activity
scene_1 = rtp.Scene()

button_1: rtp.Button = rtp.button(gui=ui, x_coord=1920/2, y_coord=1080/2)
skeleton: rtp.Skeleton = rtp.skeleton(gui=ui)

scene_1.add_component(button_1)
scene_1.add_component(skeleton)

activity.add_scene(scene_1)

# Start
activity.run()
